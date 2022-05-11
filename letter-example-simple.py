'''
Simple example. Font must be downloaded and placed in the same directory.
See: https://fonts.google.com/specimen/Press+Start+2P?category=Display#standard-styles
'''

from letterLib import blkLibrary

#Start library
blk = blkLibrary()

#Define path - create a folder - Not working!
path = 'testEmoji'

#Text to convert. One letter or emoji per block
text = '8-bit'

#Convert text to a list. Adds space in first location
blocks = list(text)

#Process list
for letter in blocks:

    #Update letter
    blk.text = letter
    blk.fontName = 'PressStart2P-Regular.ttf'

    #Create block
    blk.createBlockHelper()

    #Export as STL
    blk.exportAsSTL()
