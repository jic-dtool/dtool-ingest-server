import os
import json

from pathlib import Path

from flask import Blueprint, request
from flask.json import jsonify

from dtool_utils.quick_dataset import create_quick_dataset



DATA_DIRPATH = 'local-data/astuswrites'


bp = Blueprint("ingest", __name__, url_prefix="/ingest")


def read_tus_data_store(dirpath):

    def parse_info(info):
        idn = info['ID']
        filename = info['MetaData']['filename']
        return filename, idn

    all_files = {}
    for fpath in list(Path(dirpath).glob('*.info')):
        with open(fpath) as fh:
            info = json.load(fh)
            filename, idn = parse_info(info)
            all_files[filename] = idn

    return all_files


def tus_data_store_get_fpath(fname):
    
    files_to_identifiers = read_tus_data_store(DATA_DIRPATH)
    idn = files_to_identifiers[fname]

    suffix = '.bin'
    return os.path.join(DATA_DIRPATH, idn) + suffix


@app.route('/create', methods=['POST'])
def  create():
    create_structure = request.json

    files_to_include = create_structure['files']

    path_specifiers = [
        (tus_data_store_get_fpath(fname), fname)
        for fname in files_to_include
    ]
    name = create_structure['name']
    base_uri = create_structure['base_uri']

    app.logger.info(f'Attempting to create with name {name} at {base_uri}')

    uri = create_quick_dataset(base_uri, name, path_specifiers)

    return uri


@app.route('/dryrun', methods=['POST'])
def dryrun():

    create_structure = request.json

    print(create_structure)

    return "Good"


@app.route('/available')
def available_files():
    files = read_tus_data_store(DATA_DIRPATH)
    return jsonify(files)


@app.route('/baseuris')
def available_base_uris():
    base_uris = ['scratch', 'azure://informaticsscratch']
    return jsonify(base_uris)


@app.route('/')
def hello_world():
    return "Hello, World!"
