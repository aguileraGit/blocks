## Python Generated Blocks

Blocks are generated using Python and [Cadquery](https://cadquery.readthedocs.io/en/latest/index.html). Blocks are composed of a common 5x5 *base block*. Each top-face is unique.

The advantage to using code is avoiding repeated actions. Code to create each base is a simple line of code. Modifications can be preformed with minimal effort. Modifications, such as adding a version number to each block has to only be done once.

Currently most faces are circles, squares, rectangles, arcs, or bends. They are made to *mate* with other blocks. Future work will involve more complicated shapes and letters.

Ultimate goal is for them to be used with a small printing press. Some kind of frame will be created to hold blocks in place.

Executing the blockLib.py file will generate (9) blocks as of 3/22 and export them as STLs.

More work planned to export blocks to a single STL for easy 3D printing.

See [Provision Press](https://www.provisionalpress.com) for their simple Lego based kid friendly system. It's unclear if this would work with their press.
