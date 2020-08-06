# Functions #


def check_path(mpath=PATH):
    if os.path.isdir(mpath) and 'assets' in os.listdir(mpath):
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
def check_mods():
    # mods path
    mpath = os.path.join(PATH, 'mods')

    # Create folder if not exists and out
    if not os.path.exists(mpath):
        os.makedirs(mpath)
        mpath = os.path.join(mpath, '1.12.2')
        os.makedirs(mpath)
        return {}

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
        filename = ntpath.basename(modFile).replace(' ', '_')

        # Default values
        FILENAMES[filename] = modFile
        versions[filename] = '?'

        if 'mcmod.info' not in file.namelist():
            continue

        # Reading mod info
        try:
            mod_data = json.loads(file.read('mcmod.info'))
        except Exception as e:
            continue

        # Delete default values
        del versions[filename]
        del FILENAMES[filename]

        # Getting mod info in different mods
        if type(mod_data) is dict:
            mod_data = mod_data['modList']
        else:
            mod_data = mod_data

        # Adding mod id with version to dict
        for mod in mod_data:
            versions[mod['modid']] = mod['version']
            FILENAMES[mod['modid']] = modFile
    return versions


def check_updates(versions):
    try:
        req = requests.post(URL + 'upd/check', json=json.dumps(versions))
    except Exception:
        sys.exit(lang.get('error.server'))

    return req.json()


def delete_mods(mods):
    for mod in mods:
        if mod in FILENAMES.keys() and os.path.isfile(FILENAMES[mod]):
            os.remove(FILENAMES[mod])


def download_mods(mods):
    for mod in mods:
        try:
            wget.download(URL + 'upd/get/' + mod, os.path.join(PATH, 'mods', '1.12.2', mod))
        except Exception:
            continue
# ---------- #