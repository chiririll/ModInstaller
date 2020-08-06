import sys
import os.path

import lang
import utils

FILENAMES = {}
URL = "http://autochess.pythonanywhere.com"

if sys.platform in ['win32']:
    PATH = os.path.join(os.getenv('APPDATA'), '.minecraft')
elif sys.platform in ['linux', 'linux2']:
    PATH = os.path.expanduser('~/.minecraft')
elif sys.platform in ['darwin']:
    PATH = os.path.expanduser('~/Library/Application Support/minecraft')
else:
    sys.exit(lang.get('os.unsupported'))


# Starting #
lang.p('greeting', v="1.0")
PATH = utils.check_path(PATH)
# -------- #

# Scanning mods #
lang.p('step.scan')

# mods path
mod_path = os.path.join(PATH, 'mods')

# Getting info about client mods
data = utils.check_mods(mod_path)

lang.p('ok')
# ------------- #

# Getting updates #
lang.p('step.upd.get')
mod_path = os.path.join(mod_path, '1.12.2')
utils.update(data, mod_path)
lang.p('ok')
# -------------------- #


# Deleting old mods
lang.p('step.upd.delete')
utils.delete_mods(mod_path)
lang.p('ok')

lang.p('done')
