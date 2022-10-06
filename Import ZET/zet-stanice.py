download_url = 'https://zet.hr/gtfs-scheduled/latest'

no_dataset_id = True

source = 'Zagrebački električni tramvaj'
add_source = True

query = [('public_transport', 'platform'), ('name',)]

bbox = True

max_distance = 100

delete_unmatched = False

tag_unmatched = False

master_tags = ('gtfs:stop_id', 'official_name')

def dataset(fileobj):
    import zipfile
    import logging
    zf = zipfile.ZipFile(fileobj)
    source = zf.read('stops.txt').splitlines()
    data = []
    n = 0

    for i in source:
        line = str( i, 'utf-8' )
        splitstrings = line.split(',')
        if len(splitstrings) == 10 and splitstrings[0][0] == '"':
            tags = {
                'gtfs:stop_id': splitstrings[0].replace('"',''),
                'official_name': splitstrings[2].replace('"',''),
            }
            data.append(SourcePoint(n, float(splitstrings[4]), float(splitstrings[5]), tags))
            n += 1
    
    print(len(data))
    return data

def matches(osmtags, zettags):
    if osmtags['official_name'] != zettags['official_name']:
        return False
    return True
