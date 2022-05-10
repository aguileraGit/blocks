import cadquery as cq

class blkLibrary:

    def __init__(self, createBlock=False):

        #Overall height of the block (standard)
        self.totalHeight = 23.32

        #Font information
        self.fontSize = 3
        self.fontDistance = 1.0
        self.fontCut = False
        self.fontCombine = True
        self.fontName = "NotoEmoji-Regular.ttf"
        self.text = "!"
        self.adjX = 0
        self.adjY = 0

        #Block overall dimensions
        self.Xoutside = 4.0
        self.Youtside = 5.0

        #Block walls
        self.Lfeet = 1.6
        self.Wshort = 0.8

        #Hollow
        self.hollowX = self.Xoutside - (self.Wshort)
        self.hollowY = self.Youtside - (self.Lfeet)
        self.hollowDepth = -20.0

        #Block starts centered on the XYZ origin. These are the true 0,0,0 points
        self.originX = -1 * (self.Xoutside/2)
        self.originY = -1 * (self.Youtside/2)

        #Feet height
        self.feetHeight = 0.8

        #Keep to the standard
        self.blockHeight = self.totalHeight - self.fontDistance - self.feetHeight

        self.weepingHoleDiameter = 0.4
        self.weepingHoleLocation = self.totalHeight - self.blockHeight  + self.weepingHoleDiameter/2

        #Create Empty Block
        self.base = cq.Workplane("XY")

        if createBlock:
            createBlockHelper()


    #Creates a solid block body
    def createBaseBlockBody(self):
        self.base = self.base.box(self.Xoutside, self.Youtside, self.blockHeight,\
        centered=True)

    #Hollows out the block
    def hollowBaseBlockBody(self):
        self.base = self.base.faces(">Z").workplane().rect(self.hollowX,\
        self.hollowY).extrude(self.hollowDepth, combine='s')

    #Adds front foot
    def createFootFront(self):
        self.base = self.base.faces(">Z").workplane().moveTo(self.originX,\
        self.originY)\
            .rect(self.Xoutside, self.Lfeet/2, centered=False)\
            .workplane(offset=self.feetHeight).moveTo(self.originX, self.originY)\
            .rect(self.Xoutside, (self.Lfeet*0.2), centered=False)\
            .loft(combine=True)

    #Adds rear foot
    def createFootRear(self):
        self.base = self.base.faces(">Z").workplane(offset=-1*self.feetHeight)\
        .moveTo(self.originX, self.originY)\
            .move(0, self.Youtside)\
            .rect(self.Xoutside,-1*self.Lfeet/2, centered=False)\
            .workplane(offset=self.feetHeight).moveTo(self.originX, self.originY)\
            .move(0, self.Youtside)\
            .rect(self.Xoutside, (-1*self.Lfeet/2)*0.4, centered=False)\
            .loft(combine=True)


    def addText(self):
        self.base = self.base.faces("<Z").workplane().center(self.adjX, self.adjY)\
            .text(self.text, self.fontSize, self.fontDistance, self.fontCut, self.fontCombine,\
                  clean=True, fontPath=self.fontName)

    #Add weeping hole for 3D resin to drain while printing/cleaning
    def addWeepingHole(self):
        self.base = self.base.faces("<X[0]").workplane().moveTo(0,self.weepingHoleLocation)\
            .circle(self.weepingHoleDiameter).extrude(-1*self.Xoutside, combine='s')

    def createBlockHelper(self):
        self.base = cq.Workplane("XY")
        self.createBaseBlockBody()
        self.hollowBaseBlockBody()
        self.createFootFront()
        self.createFootRear()
        self.addText()
        self.addWeepingHole()

    #Export
    def exportAsSTL(self, stlName=None):
        if stlName == None:
            stlName = self.text + str('.stl')
        else:
            stlName = stlName + str('.stl')

        cq.exporters.export(self.base, stlName)


blk = blkLibrary()

blocks = ['D', 'i', 'e', 'g', 'o', '😵']
for letter in blocks:
    blk.text = letter
    blk.createBlockHelper()
    blk.exportAsSTL()
