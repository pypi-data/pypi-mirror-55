'''
esy.osm.pbf
===========

Low-level interface to raw OpenStreetMap Protobuf data (aka `.pbf` files).

For convenience, the toplevel module :mod:`esy.osm.pbf` links to the most
relevant classes and functions of this library:

.. autosummary::
    :nosignatures:

    ~esy.osm.pbf.file.File
    ~esy.osm.pbf.file.Node
    ~esy.osm.pbf.file.Way
    ~esy.osm.pbf.file.Relation
    ~esy.osm.pbf.file.iter_blocks
    ~esy.osm.pbf.file.read_blob
    ~esy.osm.pbf.file.iter_primitive_block
'''

from .file import (
    File, Node, Way, Relation, iter_blocks, read_blob, iter_primitive_block,
)
