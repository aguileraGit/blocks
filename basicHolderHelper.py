#Common specs
width = 5.0

#Base component
baseWorkplane = cq.Workplane("XY").rect(width, width, centered=False)
basePart = baseWorkplane.extrude(4.0).faces("<Z").shell(-0.4)
basePart = basePart.edges("|Z").fillet(0.1)


#Clone part
featurePart = basePart

#Create workplane on top plane


'''
#Inverted 1/4 Arc
featureWorkplane = featurePart.faces(">Z").workplane()\
    .lineTo(5.0, 0).lineTo(5.0, 1.0)\
    .threePointArc((2.0, 2.0), (1.0, 5.0))\
    .lineTo(0,5)\
    .close()
'''

'''
featureWorkplane = featurePart.faces(">Z").workplane()\
    .lineTo(5.0, 0)\
    .lineTo(5.0/2, 5)\
    .close()
'''


#Extrude
featurePart = featureWorkplane.extrude(1.0)\
    .edges(">Z").fillet(0.01)

#Export
#cq.exporters.export(featurePart, 'partSTL.stl')

