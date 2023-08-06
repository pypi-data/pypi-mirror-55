# esy-osm-pbf

`esy.osm.pbf` is a low-level Python library to interact with
[OpenStreetMap](https://www.openstreetmap.org) data files in the [Protocol
Buffers (PBF)](https://developers.google.com/protocol-buffers/) format.

## Usage

To count the amount of parks in the OpenStreetMap Andorra `.pbf` file (at least
according to a copy from [geofabrik](https://www.geofabrik.de/)), do this:

```python
>>> import esy.osm.pbf
>>> osm = esy.osm.pbf.File('test/andorra.osm.pbf')
>>> len([entry for entry in osm if entry.tags.get('leisure') == 'park'])
24

```

For more details, jump to the
[documentation](https://oluensdorf.gitlab.io/esy-osm-pbf).