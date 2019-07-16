import json
from pathlib import Path
import functools


def add(w, data, element, cancel=None):

    way = way_split(w)
    element = element if cancel else json.loads(element)

    node = data
    way = way[:-1] if isinstance(way[-1], int) else way

    i = 0
    try:
        for i in range(len(way)):
            node = node[way[i]]
        way_finished = True
    except KeyError:
        way_finished = False

    if not way_finished:

        node = fol = finder(way[:i], data)

        for j in range(len(way[i:]) - 1):
            fol[way[i:][j]] = {}
            fol = fol[way[i:][j]]

        fol[way[-1]] = element

        update(way[:i], data, node)

        return "/".join(map(str, way[:i+1]))

    else:
        node, index = add_to_list(node, element)

        update(way, data, node)

        return "/".join(map(str, way)) + index


def move(w, data, new_dir):

    way = way_split(w)
    new_way = way_split(new_dir)

    temp_data = finder(way, data)

    if len(way) == len(new_way):
        delete(w, data)

    way = new_way
    fol = finder(way[:-1], data)

    index = ''

    if way[-1].isnumeric():
        fol, index = add_to_list(fol, temp_data)
    elif isinstance(fol, dict):
        fol[way[-1]] = temp_data
    else:
        fol = {way[-1]: temp_data}

    update(way[:-1], data, fol)

    return w + index


def undo(text, data):

    line1, line2 = map(lambda a: a.split(": "), text.split("\n"))

    name = line1[0].lower()
    way = line1[1]
    value = line2[1]

    if name == 'add':

        delete(way, data)

    elif name == 'move':

        if len(way_split(way)) == len(way_split(value)):

            move(value, data, way)

        elif way_split(value)[:-1] == way_split(way):

            fol = finder(value, data)
            delete(way, data)

            add(way, data, fol)

        else:

            delete(value, data)

    else:

        add(way, data, value, True)


def add_to_list(dir_, element):

    if not isinstance(dir_, list):
        dir_ = [dir_]

    dir_.append(element)

    return dir_, "/" + str(len(dir_) - 1)


def way_split(dir_):

    way = [w if not w.isnumeric() else int(w) for w in dir_.split("/")]

    return way


def finder(way, folder):

    way = way if isinstance(way, list) else way_split(way)

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

    for i in range(installed + 1, final):

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

    fol, key = reduce(w, data)

    if fol == 0:
        data.update(dict([list(new_data.items())[-1]]))
    else:
        fol[key] = new_data


def delete(w, data):

    w = way_split(w)

    fol, key = reduce(w, data)
    value = fol[key]

    del fol[key]

    if isinstance(fol, list):
        if len(fol) == 1:
            update(w[:-1], data, fol[0])

    return value
