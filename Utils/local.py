import json
import ntpath
import os
import sys
from zipfile import ZipFile


# Service methods #
def get_mods_files(mpath):
    mods = []
    for mod in os.listdir(mpath):
        if os.path.isfile(os.path.join(mpath, mod)) and mod.split('.')[-1].lower() in ['jar', 'zip']:
            mods.append(os.path.join(mpath, mod))
    return mods

# =============== #


def get_mc_path():
    PATH = ''
    if sys.platform in ['win32']:
        PATH = os.path.join(os.getenv('APPDATA'), '.minecraft')
    elif sys.platform in ['linux', 'linux2']:
        PATH = os.path.expanduser('~/.minecraft')
    elif sys.platform in ['darwin']:
        PATH = os.path.expanduser('~/Library/Application Support/minecraft')

    if os.path.isdir(PATH):
        return PATH
    else:
        return ''


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
            if 'modid' not in mod.keys():
                data['?'].append(filename)
                break
            if 'version' not in mod.keys():
                mod['version'] = '?'
            data[mod['modid']] = [mod['version'], filename]
    return data
