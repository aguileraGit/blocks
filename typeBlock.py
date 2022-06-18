
class blkLibrary:

    def __init__(self):

        self.version = 0.1
        
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
        self.addChamfer()
        self.addVersion()
        self.addSerialNumber()
        
    def createText(self):
        self.base = self.base.text(self.text, self.fontSize, self.fontDistance, self.fontCut,\
                    fontPath = self.fontName, clean=True, combine='a')

    def getBB(self):
        self.bbox = self.base.val().BoundingBox()
        
    def addPadding(self):
        pass
        
    def addShoulder(self):
        self.base = self.base.faces(">Z")\
        .moveTo(self.bbox.center.x, self.bbox.center.y)\
        .rect(self.bbox.xmax-self.bbox.xmin, self.bbox.ymax-self.bbox.ymin)\
        .extrude(-1 * self.neckHeight)
        
    def calculateBodyHeight(self):
        self.bodyHeight = self.totalHeight - self.fontDistance - self.neckHeight - self.feetHeight
        print(self.bodyHeight)

    def createBody(self):
        self.base = self.base.faces(">Z").workplane(offset=-1 * self.neckHeight)\
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
        yLen = self.bbox.ylen
        by = yLen * self.yRatio
        cy = (yLen - by)/2.0
        
        
        self.base = self.base.faces(">Z").workplane(offset= -1*(self.neckHeight + self.bodyHeight))\
        .move(self.bbox.xmin, self.bbox.ymin)\
        .rect(self.bbox.xlen, cy, centered=False)\
        .workplane(offset=-1*self.feetHeight)\
        .move(self.bbox.xmin, self.bbox.ymin)\
        .rect(self.bbox.xlen, cy*self.feetLoftRatio, centered=False)\
        .loft(combine=True)
        
        self.base = self.base.faces(">Z").workplane(offset= -1*(self.neckHeight + self.bodyHeight))\
        .move(self.bbox.xmin, self.bbox.ymax)\
        .rect(self.bbox.xlen, -1*cy, centered = False)\
        .workplane(offset=-1*self.feetHeight)\
        .move(self.bbox.xmin, self.bbox.ymax)\
        .rect(self.bbox.xlen, -1*cy*self.feetLoftRatio, centered=False)\
        .loft(combine=True)
        
    def addChamfer(self):
        pass
        
    def addWeepingHole(self):
        #Get bounding box for X Face
        xFacebbox = self.base.faces(">X").val().BoundingBox()
        
        #Y loc: -1*xFacebbox.xlen + self.feetHeight + self.bodyHeight + -1*self.weepingHoleDiameter
        self.base = self.base.faces(">X").workplane()\
        .center(xFacebbox.center.y, xFacebbox.center.x)\
        .circle(self.weepingHoleDiameter)\
        .extrude(-1*self.bbox.xlen, combine='cut')
    
    def addVersion(self):
        yFacebbox = self.base.faces(">Y").val().BoundingBox()
        
        self.base = self.base.faces(">Y").workplane()\
        .moveTo(yFacebbox.center.x, yFacebbox.center.y)\
        .rect(1,1)\
        .extrude(10)

    def addSerialNumber(self):
        pass
        
#Start library
blk = blkLibrary()

blk.text = "T"

#Create block
blk.createBlockHelper()


show_object(blk.base)