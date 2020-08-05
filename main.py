import json
import ntpath
from zipfile import ZipFile

import lang
import os
import os.path

FILENAMES = {}

# Functions #

def check_path(mpath=os.path.join(os.getenv('APPDATA'), '.minecraft')):
    if os.path.isdir(mpath):
        return mpath
    else:
        lang.p('path.wrong', path=mpath)
        lang.p('path.enter')
        return check_path(input())


def get_mods_files(mpath):
    mods = []
    for mod in os.listdir(mpath):
        if os.path.isfile(os.path.join(mpath, mod)) and mod.split('.')[-1].lower() in ['jar', 'zip']:
            mods.append(os.path.join(mpath, mod))
    return mods


# Getting client mods
def check_mods(mpath):
    # Mods path
    mpath = os.path.join(mpath, 'mods')

    # Files in mods folder
    mods = get_mods_files(mpath)

    # Files in 1.12.2 folder
    mpath = os.path.join(mpath, '1.12.2')
    mods += get_mods_files(mpath)

    # Reading mcmod.info in every mod
    versions = {}
    for modFile in mods:
        # Opening mod
        file = ZipFile(modFile, 'r')
        if 'mcmod.info' not in file.namelist():
            filename = ntpath.basename(modFile).replace(' ', '_')
            versions[filename] = '?'
            continue

        # Reading mod info
        try:
            mod_data = json.loads(file.read('mcmod.info'))
        except Exception as e:
            filename = ntpath.basename(modFile).replace(' ', '_')
            versions[filename] = '?'
            continue

        # Getting mod info in different mods
        if type(mod_data) is dict:
            mod_data = mod_data['modList']
        else:
            mod_data = mod_data

        # Adding mod id with version to dict
        for mod in mod_data:
            versions[mod['modid']] = mod['version']
    return versions

# ---------- #


lang.p('greeting', v="1.0")

lang.p('step.scan')
path = check_path()
versions = check_mods(path)
lang.p('ok')

lang.p('step.upd.check')
# TODO: send mod versions to server
lang.p('ok')

lang.p('step.upd.download')
# TODO: download mods
lang.p('ok')

lang.p('done')
