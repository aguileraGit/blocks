'''
Emoji example. Font must be downloaded and placed in the same directory.
See: https://fonts.google.com/noto/specimen/Noto+Emoji?query=Noto+E

Emojis don't function like normal text. Some emojis are actually 2 or maybe
more characters. They also don't seem to render correctly. See examples below.
'''

from letterLib import blkLibrary

#Start library
blk = blkLibrary()

#Define path - create a folder - Not working!
path = 'testEmoji'

#Text to convert. One letter or emoji per block
text = '🦸' #Platform where this lies on disappears.
text = '🧑‍🍼' #Is actually ['🧑', '\u200d', '🍼']

#Convert text to a list. Adds space in first location
blocks = list(text)
print(blocks)

#Change to Emoji Font
blk.fontName = 'NotoEmoji-Regular.ttf'

#Process list
for letter in blocks:

    #Update letter
    blk.text = letter

    #Create block
    blk.createBlockHelper()

    #Export as STL
    blk.exportAsSTL()
