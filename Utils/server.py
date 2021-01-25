import requests
import json
import ntpath
import os
import sys
from zipfile import ZipFile


def get_mods_list():
    URL = os.environ.get('URL') + "/getlist"
    req = requests.get(URL)

    # Server unavailable
    if req.status_code != 200:
        return []

    print(req.text.split(';'))



def update(data, mod_path):
    URL = os.environ.get('URL') + "/upd/get"
    chunk_size = 128

    # Cleaning last update
    if os.path.exists(os.path.join(mod_path, 'mods_temp.zip')):
        os.remove(os.path.join(mod_path, 'mods_temp.zip'))

    try:
        req = requests.post(URL, json=json.dumps(data), stream=True)
    except Exception:
        sys.exit(lang.get('error.server'))

    # Downloading zip file
    try:
        with open(os.path.join(mod_path, 'mods_temp.zip'), 'wb') as fd:
            for chunk in req.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
    except Exception:
        sys.exit(lang.get('error.download'))

    # Unpacking mods
    temp = ZipFile(os.path.join(mod_path, 'mods_temp.zip'))
    temp.extractall(mod_path)


def delete_mods(mod_path):
    # Deleting archive
    if os.path.exists(os.path.join(mod_path, 'mods_temp.zip')):
        os.remove(os.path.join(mod_path, 'mods_temp.zip'))
    try:
        file = open(os.path.join(mod_path, 'delete_mods.tmp'), 'r')
    except FileNotFoundError:
        return

    for mod in file.readlines():
        mod = mod.replace('\n', '')
        mp = os.path.join(mod_path, mod)
        if os.path.isfile(mp):
            os.remove(mp)
    file.close()
    os.remove(os.path.join(mod_path, 'delete_mods.tmp'))


def get_updates(client_mods, server_mods):
    delete = []
    update = []

    # Finding differences
    for key in server_mods.keys():
        if key == '?':
            continue
        if key not in client_mods.keys():
            update.append(server_mods[key][1])
        elif client_mods[key][0] != server_mods[key][0]:
            update.append(server_mods[key][1])
            delete.append(client_mods[key][1])

    # Handling unknown mods
    if '?' in client_mods.keys():
        new_mods = json.load(open("Unknown_Mods.json", 'r'))
        for mod in client_mods['?']:
            if mod in new_mods.keys():
                if new_mods[mod] not in update:
                    update.append(new_mods[mod])
                if mod not in delete:
                    delete.append(mod)

    return {'delete': delete, 'update': update}
