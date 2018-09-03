# STLizer

Python Module for creating STL files

## Features

### Easy-To-Use Module

Initialize stl solid object:

    stl_object = stlizer.solid(w=10, l=10, h=10)
    
Add a face:

    stl_object.add_polygon(stlizer.trigon((0, 0, 0), (1, 0, 0), (0, 0, 1)).return_poly())

Export Solid:

    stl_object.export('/Your/File/Here.stl')

