import json
from pathlib import Path
import functools


def add(w, data, element):

    way = way_split(w)
    element = json.loads(element)

    node = data['settings']

    try:
        for i in range(len(way)):
            node = node[way[i]]
        way_finished = True
    except KeyError:
        way_finished = False

    if not way_finished:

        node = fol = finder(way[:i], data['settings'])

        for j in range(len(way[i:])-1):
            fol[way[i:][j]] = {}
            fol = fol[way[i:][j]]

        fol[way[-1]] = element

        update(way[:i], data, node)

    else:

        node = add_to_list(node, element)

        update(way, data, node)


def move(w, data, new_dir):

    way = way_split(w)
    new_way = way_split(new_dir)

    temp_data = finder(way, data['settings'])
                            
    if len(way) == len(new_way):
        delete(w, data)

    way = new_way
    fol = finder(way[:-1], data['settings'])

    if way[-1].isnumeric():
        fol = add_to_list(fol, temp_data)
    elif isinstance(fol, dict):
        fol[way[-1]] = temp_data
    else:
        fol = {way[-1]: temp_data}

    update(way[:-1], data, fol)


def add_to_list(dir_, element):

    if not isinstance(dir_, list):
        dir_ = [dir_]

    dir_.append(element)

    return dir_


def way_split(dir_):

    way = [w if not w.isnumeric() else int(w) for w in dir_.split("/")]

    return way

        
def finder(way, folder):

    for f in way:
        folder = folder[f]

    return folder


def setup(file):

    with open('changes.json', 'r') as f:
        versions = json.loads(f.read())

    path = Path(file)

    with open(path, 'r') as jr:
        data = json.loads(jr.read())

    installed = list(versions).index(data['settings_version'])
    final = len(versions)

    for i in range(installed+1, final):

        changes = versions[list(versions)[i]]
        data['settings_version'] = list(versions)[i]
        
        for change in changes:

            keys = list(change.keys())
            values = list(change.values())

            if len(keys) == 2:
                globals()[keys[0]](values[0], data, values[1])
            else:
                globals()[keys[0]](values[0], data)

        with open(path, 'w') as jw:
            json.dump(data, jw, indent=2, ensure_ascii=False)


def reduce(way, data):

    if len(way) != 0:
        dir_ = functools.reduce(lambda node, key: node[key], way[:-1], data)
        return dir_, way[-1]
    else:
        return 0, 0


def update(w, data, new_data):

    fol, key = reduce(w, data['settings'])

    if fol == 0:
        data['settings'] = new_data
    else:
        fol[key] = new_data


def delete(w, data):

    w = way_split(w)
    
    fol, key = reduce(w, data['settings'])
    del fol[key]
