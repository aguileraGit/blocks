#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#imports

class blockTemplate():
    def __init__(self, description=None, workplane=None, part=None):
        self.description = None
        if description != None:
            self.description = description
            
        self.workplane = None
        if workplane != None:
            self.workplane = workplane
            
        self.part = None
        if part != None:
            self.part = part
        
        self.top = None
        self.block = None
        

class blkLibrary(): 
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
        
        self.baseBlock = {'fn': self.prtBaseBlock,
                          'description': 'Base 5x4 block',
                          'workplane': self.baseWorkplane,
                          'part': self.basepart}

        #List of all pre-made blocks. Will be generated later.
        self.defaultBlocks = [self.prtFnLargeCircle,
                              self.prtFnSemiCircleLarge,
                              self.prtFnQuarterCircleLarge
                             ]

        
        #Generate the base
        self.generateBaseBlock():
            pass

        #Generate pre-made blocks
        for blk in self.defaultBlocks:
            blk()
              
    #Create Base Block to be used later on for all parts
    def self.generateBaseBlock(self):
        #Create workplane
        #Extrude workplane
        pass
        
        
    #Takes a 2D workplane and returns a 3D part. Intended to be used with Top.
    def self.generateTop(self, workplane, height=self.topHeight):
        #returns part
        pass

    
    #Combines 3D Top and Base. 
    def self.generatePart(self, TopPart, base=self.basepart['part'], fillet=True):
        
        if fillet:
            self.filletPart()
        pass

    
    def self.filletPart(self, radius=self.filletRadius):
        pass

    
    def self.prtFnLargeCircle(self):
        self.partLargeCircle = blockTemplate()
        self.partLargeCircle.description = 'Large Circle'
        
        self.partLargeCircle.workplane = cq.Workplane("XY").center( (self.baseWidth/2),(self.baseWidth/2) ).circle(self.baseWidth)

    
    def self.prtFnSemiCircleLarge(self):
        self.partSemiCircleLarge = blockTemplate()
        self.partSemiCircleLarge.description = 'Large Semi Circle'
        #Add to blockList? What to add?

        #2D stuff here
        self.partSemiCircleLarge.workplane = 'Code For Workplane'

        #3D stuff here - Only top part
        self.partSemiCircleLarge.top = self.generateTop(self.partSemiCircleLarge.workplane)
        
        #Combine top and base - Adds fillets
        self.partSemiCircleLarge.part = self.generatePart(self.partSemiCircleLarge.top)
        

