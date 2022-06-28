'''
Simple example. Font can be downloaded directly from Google.
Font can also be placed in the directory.
'''

from letterLib import blkLibrary

#Start library
blk = blkLibrary()

#Make font smaller
blk.fontSize = 16

#Download Font from Google Fonts
fontName = blk.getGoogleFont('Monoton')

#Print actual name downloaded from Google Fonts
print('Full Font Name: ' + fontName)

#FontName can be 'Creepster' or 'Creepster.ttf' or 'Creepster-Regular.ttf'
blk.setFontName('Monoton')

#Text to convert. One letter or emoji per block
text = 'EMILIO'

#Convert text to a list.
blocks = list(text)

#Process list
for letter in blocks:

    #Update letter
    blk.text = letter

    #Create block
    blk.createBlockHelper()

    #Export as STL
    blk.exportAsSTL()
