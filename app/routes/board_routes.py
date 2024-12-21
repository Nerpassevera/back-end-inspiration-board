from flask import Blueprint, request
from app.routes.route_utilities import create_class_instance
from app.models.board import Board
bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@bp.get('/')
def get_all_boards():
    return 'all boards'


@bp.post('/')
def create_board():
    return create_class_instance(Board, request, ["title", "owner"])
