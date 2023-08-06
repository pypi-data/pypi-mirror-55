
# Download Client for Berlin Geländemodelle

Downloads [Berlins' height information](https://www.stadtentwicklung.berlin.de/geoinformation/landesvermessung/atkis/de/dgm.shtml) (Digitale Geländemodelle – ATKIS DGM - Höheninformationen), can compress them on the fly, and creates GeoJSON, CSV or txt files if desired.

**Documentation:** https://berlin-gelaendemodelle-downloader.readthedocs.io/en/latest/


## What means 'Compress'

Compression means tiles, shaped as windows, are averaged. Because one subset of the data is of shape `2000x2000`, the tile size, argument `compress`, have to divide 2000 without remainder.

The following image ([Original](http://fbarc.stadt-berlin.de/FIS_Broker_Atom//Blattschnitte/2X2_EPSG_25833.gif)) shows the structure of the data subsets (tiles).

![Data Tiles](http://fbarc.stadt-berlin.de/FIS_Broker_Atom//Blattschnitte/2X2_EPSG_25833.gif)


## Getting Started

Install the package
```bash
pip3 install berlin-opendata-downloader
```

Run the client (example):
```bash
berlin_downloader download ~/berlin_height --compress 5 --keep_original --file-format csv --file-format geojson
```


## Thank You! :heart:

Many thanks to [chrisschroer](https://github.com/chrisschroer) for the offline discussions and contributions.


## Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
