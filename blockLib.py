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
        self.baseBlock = {'description': 'Base 5x4 block',
                          'workplane': self.baseWorkplane,
                          'part': self.basePart}


        #List of all pre-made blocks. Will be generated later.
        self.defaultBlocks = [self.prtFnLargeCircle,
                              #self.prtFnSemiCircleLarge,
                              #self.prtFnQuarterCircleLarge
                             ]

        self.blocks = []

        #Generate the base
        self.baseWorkplane, self.basePart = self.generateBaseBlock()

        #Generate pre-made blocks
        for blk in self.defaultBlocks:
            blk()

    #Create Base Block to be used later on for all parts
    def generateBaseBlock(self):
        #Create workplane
        baseWorkplane = cq.Workplane("XY").rect(self.baseWidth,
                             self.baseWidth, centered=False)

        #Extrude workplane
        basePart = baseWorkplane.extrude(self.baseHeight)

        return baseWorkplane, basePart


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
        unUsedPlane, self.partLargeCircle.block = self.generateBaseBlock()

        #Create Workplane on Top (Z) face
        self.partLargeCircle.workplane = self.partLargeCircle.block.faces(">Z").workplane().center( (self.baseWidth/2),(self.baseWidth/2) ).circle(self.baseWidth/2)

        #Extrude Part
        self.partLargeCircle.block = self.partLargeCircle.workplane.extrude(self.topHeight)

        #Fillet
        #self.partLargeCircle.block = self.filletPart(self.partLargeCircle.block)

        #Add to list of blocks
        self.blocks.append(self.partLargeCircle)

    def prtFnSemiCircleLarge(self):
        self.partSemiCircleLarge = blockTemplate()
        self.partSemiCircleLarge.description = 'Large Semi Circle'
        #Add to blockList? What to add?

        #2D stuff here
        self.partSemiCircleLarge.workplane = 'Code For Workplane'

        #3D stuff here - Only top part
        self.partSemiCircleLarge.top = self.generateTop(self.partSemiCircleLarge.workplane)

        #Combine top and base - Adds fillets
        self.partSemiCircleLarge.part = self.generatePart(self.partSemiCircleLarge.top)

blk = blkLibrary()

print(blk.blocks)

for _blk in blk.blocks:
    print(_blk.name)
    blk.exportToSTL(_blk)
