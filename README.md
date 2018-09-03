# STLizer

Python Module for creating STL files

## Features

### Easy-To-Use Module

Initialize stl solid object:

    stl_object = stlizer.solid(w=10, l=10, h=10)
    
Add a face:

    stl_object.add(stlizer.trigon((0, 0, 0), (1, 0, 0), (0, 0, 1)))

Export Solid:

    stl_object.export('/Your/File/Here.stl')




# User Guide

## Trigons

**Usage**: stlizer.trigon(*p1, p2, p3*)

Trigons are the smallest unit when it comes to representing a solid in STLizer. They are the representation of triangular polygons on the 3D plane.

To make a Trigon:

    trigon = stlizer.trigon((0, 0, 0), (1, 0, 0), (0, 0, 1))
    
    
Trigons have a *whoami()* of 'trigon'.
#### trigon.split(*point*)

Returns a Polygon object containing three trigon objects pivoting from *point*. 

Example:

    trigon = stlizer.trigon((0, 0, 0), (1, 0, 0), (0, 0, 1))
    polygon = trigon.split((0.3, 0, 0.6))
    

## Polygons

**Usage**: stlizer.polygon(\**points*)

Polygons are objects representing complex polygons with more than 3 vertices.

To make a Polygon:

    polygon = stlizer.polygon((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)) # Represents a square
    
Polygons have a *whoami()* of 'trigon'.

#### polygon.add_points(\**points*)

Appends all values of *points* to *polygon.points*, then runs *polygon.initialize*.

## Semisolid datatypes

There are two types of semisolids (all classes containing the word 'solid' except for the 'solid' datatype): 
simple_solid and complex_solid.

### Figure

All semisolids are subclasses of *figure* and have a *whoami* of 'figure'.

### Simple solids

Simple solids are semisolids that are optimized for representing semisolids with few numbers of vertices. Due to the way they are programmed, you cannot represent a concave figure using *simple_solid*.

To make a simple solid:

    simple = stlizer.simple_solid((0, 0, 0), (1, 0, 0), (0, 0, 1), (1, 1, 1))


### Complex solids

Complex solids are semisolids that are constructed using trigons instead of points. Due to this difference, complex solids can represent concave figures.

To make a complex solid:

    complex = stlizer.complex_solid(*stlizer.simple_solid((0, 0, 0), (1, 0, 0), (0, 0, 1), (1, 1, 1)).ret())
    
#### complex_solid.add_simple(\**simples*)

Appends all trigon values in *simples* to *complex_solid.trigons*.








