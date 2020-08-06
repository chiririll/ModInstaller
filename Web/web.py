import json
import os

from flask import Flask, request, send_file
from zipfile import ZipFile
import utils

app = Flask(__name__)


@app.route('/mods/upd/get', methods=['GET', 'POST'])
def upd_get():
    client_mods = json.loads(request.get_json())
    server_mods = utils.check_mods('mods')

    if not client_mods:
        client_mods = {}

    data = utils.get_updates(client_mods, server_mods)

    # Creating archive
    if os.path.exists('tmp/mods.zip'):
        os.remove('tmp/mods.zip')
    if os.path.exists('tmp/delete_mods.tmp'):
        os.remove('tmp/delete_mods.tmp')

    del_mods = open('tmp/delete_mods.tmp', 'w')
    del_mods.write('\n'.join(data['delete']))
    del_mods.close()

    mods = ZipFile('tmp/mods.zip', 'w')
    mods.write('tmp/delete_mods.tmp', 'delete_mods.tmp')
    for mod in data['update']:
        mods.write(f'mods/{mod}', mod)
    mods.close()

    return send_file('tmp/mods.zip', attachment_filename='mods_temp.zip')


if __name__ == '__main__':
    app.run()
