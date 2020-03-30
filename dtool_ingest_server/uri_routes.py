from flask import (
    Blueprint,
    request,
    jsonify
)


bp = Blueprint("uris", __name__, url_prefix="/uris")


@bp.route('/baseuris')
def available_base_uris():
    base_uris = ['scratch', 'azure://informaticsscratch']
    return jsonify(base_uris)
