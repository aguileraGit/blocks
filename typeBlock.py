
totalHeight = 23.32

fontSize = 70
fontDistance = 1.0
fontCut = False

adjX = 0.0 #-0.3
adjY = 0.1 #0.7

Xoutside = 40.0
Youtside = 60.0

Lfeet = 10.6
Wshort = 10.8

hollowX = Xoutside - (Wshort)
hollowY = Youtside - (Lfeet)
hollowDepth = -12.0

originX = -1 * (Xoutside/2)
originY = -1 * (Youtside/2)

feetHeight = 4.8

#Keep to the standard
blockHeight = totalHeight - fontDistance - feetHeight

#Create Base
base = cq.Workplane("XY")
base = base.box(Xoutside, Youtside, blockHeight, centered=True)

#Cut center out from the bottom
base = base.faces(">Z").workplane().rect(hollowX,hollowY).extrude(hollowDepth, combine='s')

#Foot
base = base.faces(">Z").workplane().moveTo(originX, originY)\
    .rect(Xoutside,Lfeet/2, centered=False)\
    .workplane(offset=feetHeight).moveTo(originX, originY)\
    .rect(Xoutside, (Lfeet*0.2), centered=False)\
    .loft(combine=True)

#Other foot
base = base.faces(">Z").workplane(offset=-1*feetHeight).moveTo(originX, originY)\
    .move(0, Youtside)\
    .rect(Xoutside,-1*Lfeet/2, centered=False)\
    .workplane(offset=feetHeight).moveTo(originX, originY)\
    .move(0, Youtside)\
    .rect(Xoutside, (-1*Lfeet/2)*0.4, centered=False)\
    .loft(combine=True)

#Text
base = base.faces("<Z").workplane().center(adjX,adjY)\
    .text("A", fontSize, fontDistance, fontCut, \
          clean=True, fontPath="Creepster-Regular.ttf",\
              combine='a')

#Weeping Hole
weepingHoleDiameter = 0.4
weepingHoleLocation = totalHeight - blockHeight  + weepingHoleDiameter/2

base = base.faces("<X[0]").workplane().moveTo(0,weepingHoleLocation)\
    .circle(weepingHoleDiameter).extrude(-1*Xoutside, combine='s')


#Assembly
assy = cq.Assembly()

box = cq.Solid.makeBox(10, 10, 10)

assy.add(base, name="base0", color=cq.Color("green") )

assy.add(box, name="box1", color=cq.Color("blue"),\
         loc=cq.Location(cq.Vector(30, 0, 0)))

show_object(assy)
assy.save('assembly.step')

#Export
#cq.exporters.export(assy, 'testLetter.stl')

