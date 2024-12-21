from flask import Blueprint

bp = Blueprint("board", __name__)

@bp.get('/')
def get_all_boards():
    return 'all boards'
