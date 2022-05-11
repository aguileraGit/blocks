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
