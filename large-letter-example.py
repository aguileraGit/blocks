'''
Simple example. Font can be downloaded directly from Google.
Font can also be placed in the directory.
'''

from letterLib import blkLibrary

#Start library
blk = blkLibrary()

#Download Font from Google Fonts
fontName = blk.getGoogleFont('Rubik Moonrocks')

#FontName can be 'Creepster' or 'Creepster.ttf' or 'Creepster-Regular.ttf'
blk.setFontName('Rubik Moonrocks')

#Text to convert. One letter or emoji per block
text = 'Large'

#Convert text to a list.
blocks = list(text)

#Update font size
blk.fontSize = 36

#Increase font dept (mm)
blk.fontDistance = 2.0

#Increase wall thickness
blk.xRatio = 0.8
blk.yRatio = 0.6

#Change weeping hole diameter (mm)
blk.weepingHoleDiameter = 3.0

#Process list
for letter in blocks:

    #Update letter
    blk.text = letter

    #Create block
    blk.createBlockHelper()

    #Export as STL
    blk.exportAsSTL()
