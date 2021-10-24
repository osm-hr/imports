download_url = 'http://52.178.158.152/api/file/skole_os.csv'

dataset_id = 'e-matica'

source = 'E-Matica'
add_source = True

query = [('amenity', 'school')]

bbox = True

delete_unmatched = False

tag_unmatched = False

master_tags = ('addr:postcode','name')

max_distance = 10000

def dataset(fileobj):
    import csv
    import logging
    import random
    import requests
    import json
    
    NOMINATIM_SERVER = 'http://nominatim:8080/'
    
    byte_str = fileobj.read()
    csvText = byte_str.decode('UTF-8').splitlines()
    del csvText[0:1]
    csvreader = csv.reader(csvText, delimiter=';', quotechar='"')
    
    data = []
    n = 0
    for row in csvreader:
        tags = {
            'ref:e-matica': row[0],
            'name': row[1],
        }

        nominatim_query=NOMINATIM_SERVER + 'search.php?'

        #payload={'format':'jsonv2','city':row[4]}
        payload={'format':'jsonv2','q':row[4]}
        r = requests.get(nominatim_query, params=payload)
        prettyr=r.content.decode("utf-8", errors="replace")

        coord = (json.loads(prettyr))[0]

        data.append(SourcePoint(row[0], float(coord['lat']), float(coord['lon']), tags))
        n += 1

    print(len(data))
    return data
