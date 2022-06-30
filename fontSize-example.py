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

#Increase font dept (mm)
blk.fontDistance = 1.0

#Just print a J
blk.text = 'J'

fontSizes = [48] #48, 32, 12, 8

#Process list
for letterSize in fontSizes:

    #Update letter
    blk.fontSize = letterSize

    #Create block
    blk.createBlockHelper()

    #Export as STL
    blk.exportAsSTL()
