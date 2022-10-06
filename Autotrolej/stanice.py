download_url = 'https://gt.autotrolej.hr/google-transit.zip'

no_dataset_id = True

source = 'Autotrolej'
add_source = True

query = [('highway', 'bus_stop'), ('name',)]

bbox = True

max_distance = 40

delete_unmatched = False

tag_unmatched = False

master_tags = ('gtfs:stop_id', 'official_name')

def dataset(fileobj):
    import zipfile
    import logging
    zf = zipfile.ZipFile(fileobj)
    source = zf.read('stops.txt').splitlines()
    stop_times = str(zf.read('stop_times.txt'))
    data = []
    n = 0

    for i in source:
        line = str( i, 'utf-8' )
        splitstrings = line.split(',')
        stop_id = splitstrings[0].replace('"','')
        if len(splitstrings) == 4 and splitstrings[0][0] != 's' and (','+stop_id+',') in stop_times:
            print(splitstrings[1])
            tags = {
                'gtfs:stop_id': stop_id,
                'official_name': splitstrings[1].replace('  ', ' '),
                'bus': 'yes',
                'highway': 'bus_stop',
                'name': splitstrings[1],
                'public_transport': 'platform'
            }
            data.append(SourcePoint(n, float(splitstrings[2]), float(splitstrings[3]), tags))
            n += 1
    
    print(len(data))
    return data
