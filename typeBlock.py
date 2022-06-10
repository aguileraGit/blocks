
'''
fontSize = 5.6
fontDistance = 1.0
fontCut = False

#Text
base = cq.Workplane("XY").text("P", fontSize, fontDistance, fontCut,\
    clean=True, combine='a')


# Show the bounding box to get 'shift' 
bbox = base.val().BoundingBox()

# cen = text.val().CenterOfBoundBox() # Alternative method of getting the center.
base = base.faces(">Z")\
    .moveTo(bbox.center.x, bbox.center.y)\
    .rect(bbox.xmax-bbox.xmin, bbox.ymax-bbox.ymin)\
    .extrude(-5)
'''

class blkLibrary:

    def __init__(self):

        #Overall height of the block (standard)
        self.totalHeight = 23.32

        #Font information
        self.fontSize = 4
        self.fontDistance = 1.0
        self.fontCut = False
        self.fontCombine = True
        self.fontName = "NotoEmoji-Regular.ttf"
        self.text = "!"
        self.adjX = 0
        self.adjY = 0
        
    def createBlockHelper(self):
        self.base = cq.Workplane("XY")
        self.createText()
        self.getBB()
        self.addNeck()
        
    def createText(self):
        self.base = self.base.text(self.text, self.fontSize, self.fontDistance, self.fontCut,\
                    fontPath = self.fontName, clean=True, combine='a')

    def getBB(self):
        self.bbox = self.base.val().BoundingBox()
        
    def addNeck(self):
        self.base = self.base.faces(">Z")\
        .moveTo(self.bbox.center.x, self.bbox.center.y)\
        .rect(self.bbox.xmax-self.bbox.xmin, self.bbox.ymax-self.bbox.ymin)\
        .extrude(-5)
        
        
        
#Start library
blk = blkLibrary()

blk.text = "😀"

#Create block
blk.createBlockHelper()


show_object(blk.base)