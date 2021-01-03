download_url = 'http://0.0.0.0:8080/kucni_brojevi-sorted-4326.geojson'

no_dataset_id = True

source = 'DGU'
add_source = True

query = [('building',)]

bbox = True

max_distance = 30

delete_unmatched = False

tag_unmatched = False

master_tags = ('addr:housenumber', 'addr:street')

def dataset(fileobj):
    import logging
    import json
    
    data = []
    n = 0
    adrese = json.load(fileobj)
    for p in adrese['features']:
        if p['geometry']['type'] != 'Point':
            print('Not a point')
        #print(str(p['geometry']['coordinates'][0])+" : "+str(p['geometry']['coordinates'][1]))
        tags = {
                'addr:housenumber': p['properties']['KB'],
                'addr:street': p['properties']['UL_IME'],
                'addr:place': p['properties']['NA_IME'],
            }
        data.append(SourcePoint(n, float(p['geometry']['coordinates'][1]), float(p['geometry']['coordinates'][0]), tags))
        n += 1


    
    
    print(len(data))
    return data

#def matches(osmtags, zettags):
#    if 'gtfs:stop_id' in osmtags:
#        return False
#    if osmtags['name'][0] != zettags['official_name'][0]:
#        return False
#    return True
