from flask import Blueprint, request
from app.routes.route_utilities import *
from app.models.board import Board
from app.models.card import Card
from app.db import db

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


@bp.get("/<board_id>/cards")
def get_task_of_board(board_id):
    board = validate_model(Board, board_id)

    return {
        "id": board.id,
        "owner": board.owner,
        "title": board.title,
        "cards": [card.to_dict() for card in board.cards]
    }


@bp.post("/<board_id>/cards")
def create_card_for_board(board_id):

    new_card = create_class_instance(Card, request, ["message", "owner"], {"board_id": board_id})[0]["card"]
    send_card_created_message(new_card["message"])

    return new_card
