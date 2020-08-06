from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/upd/check', methods=['GET', 'POST'])
def upd_check():
    data = request.get_json()
    # TODO: handle data
    return jsonify({"delete": ["file1", "file2"], "download": ["file1", "file2"]})


@app.route('/upd/get/<mod>')
def upd_get(mod):
    # TODO: return mod file
    return 'Update get ' + mod + '!'


if __name__ == '__main__':
    app.run()
