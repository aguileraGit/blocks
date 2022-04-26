#Common specs
innerWidth = 50
innerLength = 100
borderWidth = 10


result = cq.Workplane().box(8, 8, 8).faces(">Z").workplane()\
    .text("Z", 10, 1.0, False, True, fontPath="Bangers-Regular.ttf")

'''
#Base component
holder = cq.Workplane("XY").rect(innerWidth+borderWidth,\
                                innerLength+borderWidth,\
                                centered=True).extrude(10)
    
holder = holder.faces(">Z").workplane().rect(innerWidth,\
                                innerLength,\
                                centered=True).cutThruAll(10)
'''

#
#Create workplane on top plane
'''
featureWorkplane = featurePart.faces(">Z").workplane()\
    .lineTo(5.0, 0)\
    .lineTo(5.0/2, 5)\
    .close()
'''







#Extrude
#featurePart = featureWorkplane.extrude(1.0)\
#    .edges(">Z").fillet(0.01)

#Export
#cq.exporters.export(featurePart, 'partSTL.stl')

