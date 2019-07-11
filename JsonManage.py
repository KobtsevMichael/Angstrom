import json
from pathlib import Path
import functools
from VersionChange import versions

def add(way, element):

    if not isinstance(way, list):
        way = [way]

    way.append(element)

    return way

def create_dir(way, node, element):

    data = node
    try:
        for i in range(len(way)):
            node = node[way[i]]
    except KeyError:
        fol = finder(way[:i], data)

    dir_ = fol

    for j in range(len(way[i:])-1):
        fol[way[i:][j]] = {}
        fol = fol[way[i:][j]]

    fol[way[-1]] = element

    return way[:i], dir_

def move(way, data, updates):

    temp_data = finder(way, data['settings'])
                            
    try:
        way = way_split(updates['To'])
    except KeyError:
        delete(data, way)
        way.pop(-1)
        way.append(updates['Rename'])

    fol = finder(way[:-1], data['settings'])

    if way[-1].isnumeric():
        fol = add(fol, temp_data)
    elif isinstance(fol, dict):
        fol[way[-1]] = temp_data
    else:
        fol = {way[-1]: temp_data}
    
    return way[:-1], fol

def way_split(dir_):

    way = [w if not w.isnumeric() else int(w) for w in dir_.split("/")]

    return way
        
def finder(way, folder):

    for f in way:
        folder = folder[f]

    return folder

def setup(file):

    path = Path(file) 

    with open(path, 'r') as jr:
        data = json.loads(jr.read())

    installed = list(versions).index(data['settings_version'])
    final = len(versions)

    for i in range(installed+1, final):
        
        with open(path, 'w') as jw:

            vers = versions[list(versions)[i]]
            data['settings_version'] = list(versions)[i]
        
            for key, value in vers.items():
                for updates in value:

                    way = way_split(updates['Way'])

                    if key == 'Add':

                        node = data['settings']
                        inf = updates['Data']

                        try:
                            fol = finder(way, node)
                            new_data = add(fol, inf)
                        except KeyError:
                            way, new_data = create_dir(way, node, inf)

                        update(data, new_data, way)

                    if key == 'Delete':

                        delete(data, way)

                    if key == 'Move':
                            
                        way, new_data = move(way, data, updates)
                        update(data, new_data, way)

            json.dump(data, jw, indent = 4, ensure_ascii = False)

def reduce(way, data):

    if len(way) != 0:
        dir_ = functools.reduce(lambda node, key: node[key], way[:-1], data)
        return dir_, way[-1]
    else:
        return 0, 0

def update(data, new_data, w):

    fol, key = reduce(w, data['settings'])

    if fol == 0:
        data['settings'] = new_data
    else:
        fol[key] = new_data

def delete(data, w):
    
    fol, key = reduce(w, data['settings'])
    del fol[key]

setup('Test/basic.json')
