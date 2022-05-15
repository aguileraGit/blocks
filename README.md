## Python Generated Blocks

This project has evolved a few times.

### Background and v1 - Lego Style
The original idea stems from the [Provision Press](https://www.provisionalpress.com) and their simple Lego based kid friendly system. Piggy-backing off that, the first version were blocks are composed of a common 5x5 *base block*. Each printable face is unique. The Blocks are generated using Python and [Cadquery](https://cadquery.readthedocs.io/en/latest/index.html).

The advantage to using code is avoiding repeated actions. Code to create each base is a simple line of code. Modifications can be preformed with minimal effort. Modifications, such as adding a version number to each block has to only be done once.

Currently most faces are circles, squares, rectangles, arcs, or bends. They are made to *mate* with other blocks. Future work will involve more complicated shapes and letters.

Executing the blockLib.py file will generate (9) blocks as of 3/22 and export them as STLs.

See [blockLib.py](https://github.com/aguileraGit/blocks/blob/main/blockLib.py) for the main library.

### v2 - Font Focus
This project moved to a more traditional printing press. The second library [letterLib.py](https://github.com/aguileraGit/blocks/blob/main/letterLib.py) allows for creation of *Type* (I think I've used that correctly). Fonts can be downloaded from [Google Fonts](https://fonts.google.com/). Using a few lines of code, an STL can be generated.

See [example](https://github.com/aguileraGit/blocks/blob/main/letter-example-simple.py) for generating letter.

With Google's new Font [https://fonts.google.com/noto/specimen/Noto+Emoji](Noto Emoji), emojis can be easily created. There are some known issues with this. See [example](https://github.com/aguileraGit/blocks/blob/main/letter-example-simple.py).

### To do
- Investigate emoji issues (multiple emojis embedded in single emoji and Z face disappearing)
- Look at Noto Font: https://fonts.google.com/noto?category=Display
- Look at Icons: https://fonts.google.com/icons?category=Display
  - Icons are in SVG. SVG has it's own set of 'commands' for creating shapes. Would need to write a converter from commands to cq commands.
- https://fonts.google.com/featured?category=Display&icon.style=Sharp
- https://fonts.google.com/featured/High-Impact+Vernacular+Display?category=Display&icon.style=Sharp
- ~It would be nice if setting a font would look for the -Regular.tff added by Google.~
- Font should look to see if file exists
- Find a way to autoscale font per block size
  - Different fonts with a single size still vary in height!
- Add example with list of dict of fontnames, offset, sizes
- Find way to export multiple blocks to a single STL
  - Able to export multiple blocks as an assembly. Can't be exported as STL.
  - https://cadquery.readthedocs.io/en/latest/assy.html
- Add image to STL
- Add pillars for very large blocks
- Look at https://github.com/michaelgale/cq-kit
- Look at https://github.com/thearn/stl_tools
