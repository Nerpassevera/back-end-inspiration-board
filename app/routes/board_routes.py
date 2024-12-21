from flask import Blueprint, request
from app.routes.route_utilities import create_class_instance, get_all_instances
from app.models.board import Board
bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@bp.get('/')
def get_all_boards():
    return get_all_instances(Board, request.args)


@bp.post('/')
def create_board():
    return create_class_instance(Board, request, ["title", "owner"])
