import requests
import lang
import json
import ntpath
import os
import sys
from zipfile import ZipFile


def check_path(mc_path):
    # Is minecraft in this folder
    if os.path.isdir(mc_path) and 'assets' in os.listdir(mc_path):
        return mc_path
    else:
        lang.p('path.wrong', path=mc_path)
        lang.p('path.enter')
        return check_path(input())


def get_mods_files(mpath):
    mods = []
    for mod in os.listdir(mpath):
        if os.path.isfile(os.path.join(mpath, mod)) and mod.split('.')[-1].lower() in ['jar', 'zip']:
            mods.append(os.path.join(mpath, mod))
    return mods


# Getting client mods
def check_mods(mod_path):
    # Create folder if not exists and out
    if not os.path.exists(mod_path):
        os.makedirs(mod_path)
        mod_path = os.path.join(mod_path, '1.12.2')
        os.makedirs(mod_path)
        return []

    # Files in mods folder
    mods = get_mods_files(mod_path)

    # Files in 1.12.2 folder
    if os.path.exists(os.path.join(mod_path, '1.12.2')):
        mod_path = os.path.join(mod_path, '1.12.2')
        mods += get_mods_files(mod_path)
    else:
        os.makedirs(os.path.join(mod_path, '1.12.2'))

    # Reading mcmod.info in every mod
    data = {}
    # data is a dict with mod id, filename and version
    # for example: { 'ic2': ['industrialcraft2-1.12.2.jar', '2.2.1'] }
    # unknown: { '?': ['filename1', 'filename2'] }

    for modFile in mods:
        # Opening mod
        file = ZipFile(modFile, 'r')
        filename = ntpath.basename(modFile).replace(' ', '_')

        if '?' not in data.keys():
            data['?'] = []

        if 'mcmod.info' not in file.namelist():
            data['?'].append(filename)
            continue

        # Reading mod info
        try:
            mod_data = json.loads(file.read('mcmod.info'))
        except Exception as e:
            data['?'].append(filename)
            continue

        # Getting mod info in different mods
        if type(mod_data) is dict:
            # In some mods json is not an array
            mod_data = mod_data['modList']

        # Adding mod id with version to dict
        for mod in mod_data:
            data[mod['modid']] = [mod['version'], filename]
    return data


def update(data, mod_path):
    URL = "http://autochess.pythonanywhere.com/mods/upd/get"
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
