import cadquery as cq

class blockTemplate:
    def __init__(self, name=None, description=None, workplane=None, part=None):
        self.name = None
        if name != None:
            self.name = name

        self.description = None
        if description != None:
            self.description = description

        #Technically a workplan on a block the way the code is written
        self.workplane = None
        if workplane != None:
            self.workplane = workplane

        self.block = None
        if part != None:
            self.part = part



class blkLibrary:
    '''
    Each block base a base and top that are joined. A function defines each block.
    self.blocks ties each base/top using a dictonary. At first it is just a function. This function
    is then passed through the generateTop function. This adds the workplane to the self.blocks
    entry. The function generateBlock then extrudes the top, combines the top and base, and fillets
    the block.
    '''
    def __init__(self):
        self.baseWidth = 5.0
        self.baseHeight = 4.0
        self.topHeight = 1.0
        self.filletRadius = 0.1

        #List of all blocks generate
        self.blockList = []

        self.baseWorkplane = None
        self.basePart = None
        self.baseFilletZ = 0.125
        self.baseFilletX = 0.075

        self.baseBlock = {'description': 'Base 5x4 block',
                          'workplane': self.baseWorkplane,
                          'part': self.basePart}

        #Generate the base
        self.basePart = self.generateBaseBlock()


        #List of all pre-made blocks. Will be generated later.
        self.defaultBlocks = [self.prtFnLargeCircle,
                              self.prtFnLargeArc,
                             ]

        self.blocks = []

        #Generate pre-made blocks
        for blk in self.defaultBlocks:
            blk()
            print('Added Block: ' + str(blk))


    #Create Base Block to be used later on for all parts
    def generateBaseBlock(self):
        #Create workplane
        baseWorkplane = cq.Workplane("XY").rect(self.baseWidth,
                             self.baseWidth, centered=False)

        #Extrude workplane
        basePart = baseWorkplane.extrude(self.baseHeight).faces("<Z").shell(-0.4)
        basePart = basePart.edges("|Z").fillet(self.baseFilletZ)
        basePart = basePart.edges(">Z").fillet(self.baseFilletX)

        return basePart


    #Takes a 2D workplane and returns a 3D part. Intended to be used with Top.
    def generateTop(self, workplane, height=None):
        if height == None:
            height = self.topHeight

        toReturn = workplane.extrude(height)

        return toReturn


    #Combines 3D Top and Base.
    def generatePart(self, TopPart, fillet=True): # base=self.basepart['part'],

        #Need to figure out how to combine both top and bottom pieces
        if fillet:
            self.filletPart()
        pass


    def filletPart(self): #, radius=self.filletRadius
        pass


    def exportToSTL(self, part):
        cq.exporters.export(part.block, (str(part.name)+'.stl') )


    def prtFnLargeCircle(self):
        self.partLargeCircle = blockTemplate()
        self.partLargeCircle.name = 'Large Circle'
        self.partLargeCircle.description = 'Large circle as big as the block'

        #Clone base part
        self.partLargeCircle.block = self.generateBaseBlock()

        #Create Workplane on Top (Z) face
        #Center on Z plane
        #Draw circle
        self.partLargeCircle.workplane = self.partLargeCircle.block.faces(">Z").workplane()\
            .center( (self.baseWidth/2),(self.baseWidth/2) )\
            .circle(self.baseWidth/2)

        #Extrude Part
        #Fillet further most Z plane
        self.partLargeCircle.block = self.partLargeCircle.workplane.extrude(1.0)\
            .edges(">Z").fillet(0.05)

        #Add to list of blocks
        self.blocks.append( {'block': self.partLargeCircle} )


    def prtFnLargeArc(self):
        self.partLargeArc = blockTemplate()
        self.partLargeArc.name = 'Large Arc'
        self.partLargeArc.description = 'Arc as large as the block'

        #Clone base part
        self.partLargeArc.block = self.generateBaseBlock()

        #Create Workplane on Top (Z) face
        self.partLargeArc.workplane = self.partLargeArc.block.faces(">Z").workplane()\
            .lineTo(5.0, 0)\
            .lineTo(5.0, 1.0)\
            .radiusArc((1.0, 5.0), -4)\
            .lineTo(0, 5.0)\
            .close()

        #Extrude Part
        self.partLargeArc.block = self.partLargeArc.workplane.extrude(1.0)\
            .edges("|Z").fillet(0.1)\
            .edges(">Z").fillet(0.05)

        #Add to list of blocks
        self.blocks.append( {'block': self.partLargeArc} )


blk = blkLibrary()


for block in blk.blocks:
    print( block['block'].name)
    blk.exportToSTL(block['block'])
