download_url = 'http://0.0.0.0:8080/klipane_adrese_point.geojson'

no_dataset_id = True

source = 'DGU'
add_source = False

query = [('addr:housenumber',)]

bbox = True

max_distance = 30

tag_unmatched = {}

master_tags = ('addr:housenumber', 'source:addr', 'source:addr:date')

def dataset(fileobj):
    import logging
    import json
    
    data = []
    n = 0
    adrese = json.load(fileobj)
    for p in adrese['features']:
        if p['geometry']['type'] != 'Point':
            print('Not a point')
            continue
        #print(str(p['geometry']['coordinates'][0])+" : "+str(p['geometry']['coordinates'][1]))
        tags = {
                'addr:housenumber': p['properties']['KB'],
                'source:addr': 'DGU',
                'source:addr:date': '2021-01-01'
            }
        if p['properties']['UL_IME'] == p['properties']['NA_IME']:
            tags['addr:place'] = p['properties']['NA_IME']
        else:
            tags['addr:street'] = p['properties']['UL_IME']
        data.append(SourcePoint(n, float(p['geometry']['coordinates'][1]), float(p['geometry']['coordinates'][0]), tags))
        n += 1

    print(len(data))
    return data

def matches(osmtags, dgutags):
    if osmtags['addr:housenumber'] != dgutags['addr:housenumber']:
        return False
    if ('addr:street' in osmtags) == False:
        return False
    if (dgutags['addr:street'].lower() in osmtags['addr:street'].lower()) == False:
        return False
    print ("dgu:"+dgutags['addr:street']+" "+dgutags['addr:housenumber']+"-------------- osm:"+osmtags['addr:street']+" "+osmtags['addr:housenumber'])
    return True
