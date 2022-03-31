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
                              self.prtFnSmallArc,
                              self.prtFnRect3x5Cen,
                              self.prtFnRect1x5Cen,
                              self.prtFnRect1x5,
                              self.prtSrq3x3Cen,
                              self.prtTriIsoLarge,
                              self.partMedBend,
                              self.partLargeBend
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
        self.partLargeCircle.block = self.partLargeCircle.workplane.extrude(self.topHeight)\
            .edges(">Z").fillet(self.baseFilletX)

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
            .edges("|Z").fillet(self.baseFilletZ)\
            .edges(">Z").fillet(self.baseFilletX)

        #Add to list of blocks
        self.blocks.append( {'block': self.partLargeArc} )

    def prtFnSmallArc(self):
        self.partSmallArc = blockTemplate()
        self.partSmallArc.name = 'Small Arc'
        self.partSmallArc.description = 'Smaller Arc - 2/3 width'

        self.partSmallArc.block = self.generateBaseBlock()

        self.partSmallArc.workplane = self.partSmallArc.block.faces(">Z").workplane()\
            .lineTo(4.0, 0)\
            .lineTo(4.0, 1.0)\
            .radiusArc((1.0, 4.0), -3)\
            .lineTo(0, 4.0)\
            .close()

        self.partSmallArc.block = self.partSmallArc.workplane.extrude(self.topHeight)\
            .edges(">Z").fillet(self.baseFilletX)

        self.blocks.append( {'block': self.partSmallArc} )

    def prtFnRect3x5Cen(self):
        self.partRect3x5 = blockTemplate()
        self.partRect3x5.name = '3x5 Rectangle Centered'
        self.partRect3x5.description = '3x5 Rectangle Centered in the middle'

        self.partRect3x5.block = self.generateBaseBlock()

        self.partRect3x5.workplane = self.partRect3x5.block.faces(">Z").workplane()\
            .moveTo(2.5, 2.5)\
            .rect(1.5, 5.0)

        self.partRect3x5.block = self.partRect3x5.workplane.extrude(self.topHeight)\
            .edges("|Z").fillet(self.baseFilletX)\
            .edges(">Z").fillet(self.baseFilletX)

        self.blocks.append( {'block': self.partRect3x5} )

    def prtFnRect1x5Cen(self):
        self.partRect1x5Cen = blockTemplate()
        self.partRect1x5Cen.name = '1x5 Rectangle Centered'
        self.partRect1x5Cen.description = '1x5 Rectangle Centered in the middel'

        self.partRect1x5Cen.block = self.generateBaseBlock()

        self.partRect1x5Cen.workplane = self.partRect1x5Cen.block.faces(">Z").workplane()\
            .moveTo(2.5, 2.5)\
            .rect(1, 5.0)

        self.partRect1x5Cen.block = self.partRect1x5Cen.workplane.extrude(self.topHeight)\
            .edges("|Z").fillet(self.baseFilletX)\
            .edges(">Z").fillet(self.baseFilletX)

        self.blocks.append( {'block': self.partRect1x5Cen} )

    def prtFnRect1x5(self):
        self.partRect1x5 = blockTemplate()
        self.partRect1x5.name = '1x5 Rectangle off centered'
        self.partRect1x5.description = '1x5 Rectangle off centered'

        self.partRect1x5.block = self.generateBaseBlock()

        self.partRect1x5.workplane = self.partRect1x5.block.faces("Z").workplane()\
            .moveTo(3.5, 2.5)\
            .rect(1, 5)

        self.partRect1x5.block = self.partRect1x5.workplane.extrude(self.topHeight)\
            .edges("|Z").fillet(self.baseFilletX)\
            .edges(">Z").fillet(self.baseFilletX)

        self.blocks.append( {'block': self.partRect1x5} )

    def prtTriIsoLarge(self):
        self.partTriIso = blockTemplate()
        self.partTriIso.name = 'Isosceles Triangle. I think.'
        self.partTriIso.description = 'Isosceles Triangle centered'

        self.partTriIso.block = self.generateBaseBlock()

        self.partTriIso.workplane = self.partTriIso.block.faces("Z").workplane()\
            .lineTo(5.0, 0)\
            .lineTo(5.0/2, 5)\
            .close()

        self.partTriIso.block = self.partTriIso.workplane.extrude(self.topHeight)\
            .edges(">Z").fillet(self.baseFilletX)

        self.blocks.append( {'block': self.partTriIso} )


    def prtSrq3x3Cen(self):
        self.partSrq3x3Cen = blockTemplate()
        self.partSrq3x3Cen.name = '3x3 Square Centered'
        self.partSrq3x3Cen.description = '3x3 Squared on Center'

        self.partSrq3x3Cen.block = self.generateBaseBlock()

        self.partSrq3x3Cen.workplane = self.partSrq3x3Cen.block.faces("Z").workplane()\
            .moveTo(2.5, 2.5)\
            .rect(1.5, 1.5)

        self.partSrq3x3Cen.block = self.partSrq3x3Cen.workplane.extrude(self.topHeight)\
            .edges("|Z").fillet(self.baseFilletX)\
            .edges(">Z").fillet(self.baseFilletX)

        self.blocks.append( {'block': self.partSrq3x3Cen} )

    def partMedBend(self):
        self.partMedBend = blockTemplate()
        self.partMedBend.name = 'Medium Bend'
        self.partMedBend.description = 'Medium Bend L Shape'

        self.partMedBend.block = self.generateBaseBlock()

        self.partMedBend.workplane = self.partMedBend.block.faces("Z").workplane()\
            .lineTo(3,0)\
            .lineTo(3,2)\
            .radiusArc((2,3), -1)\
            .lineTo(0,3)\
            .lineTo(0,4)\
            .lineTo(3,4)\
            .radiusArc((4,3), 1)\
            .lineTo(4,0)\
            .lineTo(3,0)\
            .close()

        self.partMedBend.block = self.partMedBend.workplane.extrude(self.topHeight)\
            .edges("|Z").fillet(self.baseFilletX)\
            .edges(">Z").fillet(self.baseFilletX)

        self.blocks.append( {'block': self.partMedBend} )

    def partLargeBend(self):
        self.partLargeBend = blockTemplate()
        self.partLargeBend.name = 'Large Bend'
        self.partLargeBend.description = 'Maxium Bend L Shape'

        self.partLargeBend.block = self.generateBaseBlock()

        self.partLargeBend.workplane = self.partLargeBend.block.faces("Z").workplane()\
            .lineTo(4,0)\
            .lineTo(4,3)\
            .radiusArc((3,4), -1)\
            .lineTo(0,4)\
            .lineTo(0,5)\
            .lineTo(4,5)\
            .radiusArc((5,4), 1)\
            .lineTo(5,0)\
            .lineTo(4,0)\
            .close()

        self.partLargeBend.block = self.partLargeBend.workplane.extrude(self.topHeight)\
            .edges("|Z").fillet(self.baseFilletX)\
            .edges(">Z").fillet(self.baseFilletX)

        self.blocks.append( {'block': self.partLargeBend} )




blk = blkLibrary()


for block in blk.blocks:
    print( block['block'].name)
    blk.exportToSTL(block['block'])
