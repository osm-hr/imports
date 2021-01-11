download_url = 'http://0.0.0.0:8080/klipane_adrese_glina.geojson'

no_dataset_id = True

source = 'DGU'
add_source = False

query = [('addr:housenumber',)]

bbox = True

max_distance = 2

#tag_unmatched = {'fixme': 'Provjeriti adresu, nema u DGU popisu adresa'}

master_tags = ('addr:housenumber', 'source:addr', 'source:addr:date')

def dataset(fileobj):
    import re
    import json

    def croatianStreetCapitalize(string):
        # Detect ALLCAPS
        if re.match(r"^[A-Z0-9\u0110\u0160\u010C\u0106\u017D\.\ ]+$", string):
            exclude_list = ['hrvatskog plemića Vuka', 'Matice hrvatske', 'Hrvatskog proljeća', 'ulica', 'odvojak', 'cesta', 'avenija', 'trg', 'prilaz', 'naselja', 'novog', 'desni', 'lijevi', 'dr.', 'narodnih', 'učitelja', 'zelenila', 'kneza', 'bana', 'kralja', 'rata', 'žrtava', 'proljeća', 'svetog', 'kolovoza', 'dragovoljaca', 'sokola', 'bratske', 'zajednice', 'hrvatskih', 'branitelja']
            
            split_string = string.split(' ')
            processed_words=[False]*len(split_string)
            for correctCase in exclude_list:
                x = string.lower().find(correctCase.lower())
                x_word_order=string[0:x].count(' ')
                if x > -1 and not processed_words[x_word_order]:
                    string.replace(correctCase.upper(), '$')
                    split_string = (' '.join(split_string)).replace(correctCase.upper(),correctCase).split(' ')
                    for i in range(len(correctCase.split(' '))):
                        processed_words[x_word_order+i]=True
            q=0
            for processed in processed_words:
                #print ('processed: '+str(processed)+' '+ split_string[q])
                if not processed:
                    split_string[q]=split_string[q].lower().capitalize()
                    #print('Procesiram neprocesiranu riječ broj '+str(q)+' Sve je: '+str(split_string))
                q+=1        
            #print ('Prije kapitalizacije'+str(split_string))
            normalized = ' '.join(split_string)
            normalized = normalized[0].upper() + normalized[1:]
            #print (normalized)
            # ' '.join([split_string[0].title()] + [tt.title() if tt.lower() not in exclude_list else tt.lower() for tt in split_string[1:]])
            
            # Fix roman numerals I, II, III
            normalized = re.sub(r"\bIi+\b", lambda m: m.group(0).upper(), normalized)
            print("Normalizing", string, "->", normalized)
            return normalized
        return string

    data = []
    n = 0
    adrese = json.load(fileobj)
    for p in adrese['features']:
        if p['geometry']['type'] != 'Point':
            print('Not a point')
            continue
        if p['properties']['SRUSENO']=='DA':
            continue
        tags = {
                'addr:housenumber': p['properties']['KB'],
                'source:addr': 'DGU',
                'source:addr:date': '2021-01-01'
            }
        if p['properties']['UL_IME'] == p['properties']['NA_IME']:
            tags['addr:place'] = croatianStreetCapitalize(p['properties']['NA_IME'])
        else:
            tags['addr:street'] = croatianStreetCapitalize(p['properties']['UL_IME'])
        
        print (p)
        print (tags)
        data.append(SourcePoint(n, float(p['geometry']['coordinates'][1]), float(p['geometry']['coordinates'][0]), tags))
        print('dodao!')
        n += 1
    with open("data.txt", "a") as myfile:
        datastring=[]
        for entry in data:
            stringToAdd="\n"+str(entry.id)+';'+str(entry.lat)+';'+str(entry.lon)+';'+str(entry.tags)
            print(stringToAdd)
            datastring.append(stringToAdd)
        print (datastring)
        myfile.writelines(datastring)
    print(len(data))
    return data

def matches(osmtags, dgutags):
    if osmtags['addr:housenumber'] != dgutags['addr:housenumber']:
        return False
    osm_address_name = None
    dgu_address_name = None
    if 'addr:street' in osmtags:
        osm_address_name=osmtags['addr:street']
    else:
        osm_address_name=osmtags['addr:place']
    if osm_address_name == None:
        return False
    if 'addr:street' in dgutags:
        dgu_address_name = dgutags['addr:street']
    else:
        dgu_address_name = dgutags['addr:place']
    if dgu_address_name.lower() not in osm_address_name.lower():
        return False
    print ("dgu:"+dgu_address_name+" "+dgutags['addr:housenumber']+"-------------- osm:"+osm_address_name+" "+osmtags['addr:housenumber'])
    return True
