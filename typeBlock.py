
class blkLibrary:

    def __init__(self):

        self.version = "v0.2"
        self.versionTextSize = 20.0
        self.versionTextEmboss = -0.2
        
        #Overall height of the block (standard)
        self.totalHeight = 23.32

        #Font information
        self.fontSize = 28
        self.fontDistance = 1.0
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
        
        self.paddingX = 0.0
        self.paddingY = 0.0
        
        self.supportWidth = 0
        self.support = None

        
    def createBlockHelper(self, support=None):
        self.base = cq.Workplane("XY")
        self.createText()
        self.getBB()
        self.addPadding()
        self.addShoulder()
        self.calculateBodyHeight()
        self.createBody()
        self.hollowBody()
        self.createFeet()
        
        if support == 'center':
            self.addCenterSupport()
            
        self.addWeepingHole()
        self.addChamfer()
        self.addVersion()
        self.addSerialNumber()
        #self.addTopFix()
        #self.mirrorBlock()

        
        
    def createText(self):
        self.base = self.base.text(self.text, self.fontSize, self.fontDistance, self.fontCut,\
                    fontPath = self.fontName, clean=False, combine='a')
            
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
            
        
    def addShoulder(self):
        #debug(self.base.faces(">Z"))
        
        #Find the max Z height and offset down by the font distance.
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
        print(self.bodyHeight)

    def createBody(self):
        offsetDistance = -1 * (self.neckHeight + self.fontDistance)
        
        self.base = self.base.faces(">Z").workplane(offset= offsetDistance)\
        .moveTo(self.bbox.center.x, self.bbox.center.y)\
        .rect(self.bbox.xmax-self.bbox.xmin, self.bbox.ymax-self.bbox.ymin)\
        .extrude(-1 * self.bodyHeight)
        
    def hollowBody(self):
        self.base = self.base.faces("<Z")\
        .moveTo(self.bbox.center.x, self.bbox.center.y)\
        .rect( (self.bbox.xmax-self.bbox.xmin) * self.xRatio,\
               (self.bbox.ymax-self.bbox.ymin) * self.yRatio)\
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
        .center(xFacebbox.center.y, self.bodyHeight - self.weepingHoleDiameter)\
        .circle(self.weepingHoleDiameter)\
        .extrude(-1*(self.bbox.xlen+self.paddingX), combine='cut')
    
    def addVersion(self):
        self.base = self.base.faces("<X").workplane(centerOption="CenterOfMass")\
        .move(0, -1*self.bodyHeight)\
        .text(self.version, self.totalHeight/8.0, self.versionTextEmboss, self.fontCut,\
              fontPath = None, clean=True, combine='cut')
        
    def addSerialNumber(self):
        pass
    
    def addTopFix(self):
        self.base = self.base.faces("<Z[2]").workplane(centerOption="CenterOfMass")\
        .moveTo(self.bbox.center.x, self.bbox.center.y)\
        .rect(self.bbox.xmax-self.bbox.xmin, self.bbox.ymax-self.bbox.ymin)\
        .extrude(-1 * self.neckHeight, combine='a')
        
    def addCenterSupport(self):
        centerSupportWidth = (self.bbox.ymax-self.bbox.ymin) * self.yRatio

        self.base = self.base.faces(">Z[2]").workplane(centerOption="CenterOfMass")\
        .moveTo(self.bbox.center.x, self.bbox.center.y)\
        .rect(self.supportWidth, centerSupportWidth )\
        .extrude(1* self.bodyHeight)


        
#Start library
blk = blkLibrary()

blk.text = 'r'

blk.neckHeight = 3.0
blk.fontDistance = 2.0
#blk.paddingX = 4.0
#blk.paddingY = 2.0
#blk.fontName = 'PressStart2P-Regular.ttf'
#blk.fontName = 'OleoScript-Regular.ttf'
#blk.fontName = 'Creepster-Regular.ttf'
blk.fontName = 'Bangers-Regular.ttf'
#blk.fontName = 'NotoEmoji-Regular.ttf'

#Create block
blk.supportWidth = 1.0
blk.createBlockHelper(support='center')

#Update object
show_object(blk.base)

'''
fontDepth = 2.0

base = cq.Workplane("XY")

base = base.text('💩', 12, fontDepth, fontPath = 'NotoEmoji-Regular.ttf')

bbox = base.val().BoundingBox()

offsetDistance = -1*(fontDepth) - 0.0

base = base.faces(">Z").workplane(offset=offsetDistance)\
    .moveTo(bbox.center.x, bbox.center.y)\
    .rect(bbox.xmax-bbox.xmin, bbox.ymax-bbox.ymin)\
    .extrude(-1 * 4.0)

show_object(base)
'''
