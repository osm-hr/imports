# Importiranje ZET podataka iz GTFS-a

Trenutno imamo zet-stanice.py koji se učitava sa [OSM Conflatorom](https://github.com/mapsme/osm_conflate). Puna komanda bi bila:

`conflate -v zet-stanice.py -o josm.osm -c preview.json`

Ta komanda automatski skida GTFS datoteku sa [ove stranice](https://www.zet.hr/odredbe/datoteke-u-gtfs-formatu/669). U metodi `dataset` ju odzipa i uzme datoteku `stops.txt`, izlista sve stanice i mapira ju u tip podataka koji koristi OSM Conflator.

Varijabla `query` određuje kako će izgledati overpass upit koji će dohvatiti podatke.

U metodi `matches` ignorira elemente ako osm objekt ima tag `gtfs:stop_id`, ili ako tag `name` ne počinje sa istim slovom kao i stanica u gtfs-u.

`max_distance` govori koliko daleko od stanice u GTFS-u se traži stanica iz OSM-a.

Na kraju dobivamo datoteke `josm.osm` koja u sebi ima changeset koji [Josm](https://josm.openstreetmap.de/) može poslati u bazu OSM-a.

`preview.json` je geojson koji se može učitati na [geojson.io](http://geojson.io) i koji će na karti pokazati gdje se točke dodaju, gdje se mjenjaju, a gdje brišu. 
