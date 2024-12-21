from flask import Blueprint, request
from app.routes.route_utilities import create_class_instance, get_all_instances, get_one_instance, delete_instance, update_instance
from app.models.board import Board
bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@bp.get('/')
def get_all_boards():
    return get_all_instances(Board, request.args)


@bp.post('/')
def create_board():
    return create_class_instance(Board, request, ["title", "owner"])

@bp.get("/<board_id>", strict_slashes=False)
def get_one_board(board_id):
    return get_one_instance(Board, board_id)

@bp.delete("/<board_id>", strict_slashes=False)
def delete_board(board_id):
    return delete_instance(Board, board_id)

@bp.put("/<board_id>", strict_slashes=False)
def update_board(board_id):
    return update_instance(Board, board_id, request)