import cadquery as cq
import requests
import zipfile
import glob
import os
import re

class blkLibrary:

    def __init__(self, createBlock=False):

        self.version = "v0.2"
        self.versionTextSize = 20.0
        self.versionTextEmboss = -0.2

        #Overall height of the block (standard)
        self.totalHeight = 23.32

        #Font information
        self.fontSize = 28
        self.fontDistance = 2.0
        self.fontCut = False
        self.fontCombine = True
        self.fontName = None
        self.text = "!"

        #Neck - Z height from the font to the body. Always solid.
        self.neckHeight = 3.0

        #Feet height
        self.feetHeight = 2.2
        self.feetLoftRatio = 0.6

        #Ratios - Define wall & feet thickness
        self.xRatio = 0.85
        self.yRatio = 0.65

        self.weepingHoleDiameter = 2.0

        self.chamferSize = 1.0

        #Add space so letters aren't right next to each other
        self.paddingX = 0.0
        self.paddingY = 0.0

        #A dictionary of dimensions - Should move it to an object
        self.dimensions = {
            'xBlockLength': 0.0,
            'yBlockLength': 0.0,
            'zBlockHeight': 0.0,
            'xWallThickness': 0.0,
            'yWallThickness': 0.0
        }

    def createBlockHelper(self):
        self.base = cq.Workplane("XY")
        self.createText()
        self.getBB()
        self.addPadding()
        self.addShoulder()
        self.calculateBodyHeight()
        self.createBody()
        self.hollowBody()
        self.createFeet()
        self.addWeepingHole()
        self.addChamfer() #Need to be written
        self.addVersion()
        self.addSerialNumber() #Needs to be written


    def createText(self):
        self.base = self.base.text(self.text, self.fontSize, self.fontDistance, self.fontCut,\
                    fontPath = self.fontName, clean=False, combine='a')

        #Mirror so you don't forget later on
        self.base = self.base.mirror(mirrorPlane="ZY")

    def getBB(self):
        self.bbox = self.base.val().BoundingBox()

    def addPadding(self):
        if self.paddingX > 0.0:
            self.bbox.xmin = self.bbox.xmin - (self.paddingX/2)
            self.bbox.xmax = self.bbox.xmax + (self.paddingX/2)

        if self.paddingY > 0.0:
            self.bbox.ymin = self.bbox.ymin - (self.paddingY/2)
            self.bbox.ymax = self.bbox.ymax + (self.paddingY/2)

        #Update dimensions
        self.dimensions['xBlockLength'] = self.bbox.xmax - self.bbox.xmin
        self.dimensions['yBlockLength'] = self.bbox.ymax - self.bbox.ymin


    def addShoulder(self):
        #This issue only seems to affect the emoji font (NotoEmoji)
        # Find the max Z height and offset down by the font distance.
        # Adding -0.1 fixes the strangeness, but leaves a gap
        # Adding +0.1
        offsetDistance = -1*(self.fontDistance) + -0.0

        self.base = self.base.faces(">Z").workplane(offset = offsetDistance)\
        .moveTo(self.bbox.center.x, self.bbox.center.y)\
        .rect(self.bbox.xmax-self.bbox.xmin, self.bbox.ymax-self.bbox.ymin)\
        .extrude(-1 * self.neckHeight, combine=True, clean=True)

        #show_object(self.base)


    def calculateBodyHeight(self):
        self.bodyHeight = self.totalHeight - self.fontDistance - self.neckHeight - self.feetHeight

        self.dimensions['zBlockHeight'] = self.totalHeight


    def createBody(self):
        offsetDistance = -1 * (self.neckHeight + self.fontDistance)

        self.base = self.base.faces(">Z").workplane(offset= offsetDistance)\
        .moveTo(self.bbox.center.x, self.bbox.center.y)\
        .rect(self.bbox.xmax-self.bbox.xmin, self.bbox.ymax-self.bbox.ymin)\
        .extrude(-1 * self.bodyHeight)


    def hollowBody(self):
        xCutOut = (self.bbox.xmax-self.bbox.xmin) * self.xRatio
        yCutOut = (self.bbox.ymax-self.bbox.ymin) * self.yRatio

        self.base = self.base.faces("<Z")\
        .moveTo(self.bbox.center.x, self.bbox.center.y)\
        .rect( xCutOut, yCutOut )\
        .extrude(-1 * self.bodyHeight, combine='cut')


    def createFeet(self):
        offsetDistance = -1 * (self.neckHeight + self.fontDistance + self.bodyHeight)

        yLen = self.bbox.ylen
        by = yLen * self.yRatio
        cy = (yLen - by)/2.0

        self.base = self.base.faces(">Z").workplane(offset = offsetDistance)\
        .move(self.bbox.xmin, self.bbox.ymin)\
        .rect(self.bbox.xlen+self.paddingX, cy, centered=False)\
        .workplane(offset=-1*self.feetHeight)\
        .move(self.bbox.xmin, self.bbox.ymin)\
        .rect(self.bbox.xlen+self.paddingX, cy*self.feetLoftRatio, centered=False)\
        .loft(combine=True)

        self.base = self.base.faces(">Z").workplane(offset= offsetDistance)\
        .move(self.bbox.xmin, self.bbox.ymax)\
        .rect(self.bbox.xlen+self.paddingX, -1*cy, centered = False)\
        .workplane(offset=-1*self.feetHeight)\
        .move(self.bbox.xmin, self.bbox.ymax)\
        .rect(self.bbox.xlen+self.paddingX, -1*cy*self.feetLoftRatio, centered=False)\
        .loft(combine=True)

    def addChamfer(self):
        pass

    def addWeepingHole(self):
        #Get bounding box for X Face
        xFacebbox = self.base.faces(">X").val().BoundingBox()

        yDist = self.feetHeight + self.bodyHeight + -1*self.weepingHoleDiameter

        self.base = self.base.faces(">X").workplane()\
        .center(xFacebbox.center.y, yDist)\
        .circle(self.weepingHoleDiameter)\
        .extrude(-1*(self.bbox.xlen+self.paddingX), combine='cut')

    def addVersion(self):
        self.base = self.base.faces("<X").workplane(centerOption="CenterOfMass")\
        .move(0, -1*self.bodyHeight)\
        .text(self.version, self.totalHeight/8.0, self.versionTextEmboss, self.fontCut,\
              fontPath = None, clean=True, combine='cut')

    def addSerialNumber(self):
        pass


    #Export as STL. Filename format: blockText_0.stl. If filename exists, function
    # will increase number. This is useful when looping through multiple blocks
    # and the same letter is repeated. Loop for example would overwrite the 'o'
    # file. When you print you would miss an 'o'.
    def exportAsSTL(self, path=None):
        if path == None:
            path = '/'
        else:
            path = '/' + path + '/'

        #Format filename: blockText_0.stl
        stlName = self.text + '_0' + str('.stl')

        #Check if file exists. If so, increase _#
        fileNumber = self.findFileinDir(stlName)

        #Update filename
        newvalue = '_' + str(fileNumber+1)
        stlName = stlName.replace('_0', newvalue)

        cq.exporters.export(self.base, stlName)


    def findFileinDir(self, fileNameInQuestion):
        #Replace _0 with re expression to find any number
        fileNameInQuestion = fileNameInQuestion.replace('_0', '_(\d{1,})')

        #Build re expression
        txtPattern = re.compile(r'{}'.format(fileNameInQuestion))

        largestValue = 0

        #Search for pattern in directory
        for file in os.listdir():
            matches = re.search(txtPattern, file)

            if matches:
                latestValue = int( matches.group(1) )

                #Update largestValue is needed
                if latestValue > largestValue:
                    largestValue = latestValue

        #Return largest value
        return largestValue


    def exportAsPart(self):
        return self.base

    #Downloads and uses Google Font
    def useGoogleFont(self, fontName):
        self.getGoogleFont(fontName)
        self.setFontName(fontName)

    #Only downloads the Google Font. Still need to call setFontName to use font
    def getGoogleFont(self, fontName):
        #Need to check if font exisits in folder

        zipFileName = fontName.replace(' ', '-') + '.zip'

        #Replace spaces with %20
        fontNameDownload = fontName.replace(' ', '%20')

        #Define url.
        url = 'https://fonts.google.com/download?family=' + fontNameDownload

        #Download
        r = requests.get(url, allow_redirects=True)

        #Write to the folder
        open(zipFileName, 'wb').write(r.content)

        #Open zip file
        fileFound = False
        with zipfile.ZipFile(zipFileName, mode="r") as archive:
            for filename in archive.namelist():
                #Look for actual font
                if filename[-4:] == '.ttf':
                    #Save font to directory
                    archive.extract(filename)

                    fileFound = True
                    return filename

        #Assert is font download/extraction isn't successful
        assert fileFound != False, f'Error extracting Font'


    #Should break this down into 2 parts. One to search directory.
    # Two. If found, set fontName.
    def setFontName(self, fontName):
        #Remove .ttf
        fontName = fontName.strip('.ttf')

        #Replace spaces with nothing
        fontName = fontName.replace(' ', '')

        print(fontName)

        reFont = re.escape(fontName) + r'(-Regular|).ttf'

        #Find all files that match
        fontName = list(filter(re.compile(reFont).match, os.listdir()))

        #Assert if font isn't found
        assert len(fontName) > 0, f'Font not found'

        #Assert if multiple fonts match
        assert len(fontName) == 1, f'Multiple fonts found'

        self.fontName = fontName[0]
