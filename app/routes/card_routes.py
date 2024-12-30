from flask import Blueprint, request
from app.routes.route_utilities import *
from app.models.card import Card
from app.models.board import Board

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

#  Ask FE team if this route is needed. If yes - add it to README
@bp.get('/')
def get_all_cards():
    return get_all_instances(Card, request.args)


@bp.get('/<card_id>')
def get_one_card(card_id):
    return get_one_instance(Card, card_id)

# # added this card... goes with 
# @bp.patch("/<board_id>/cards")
# def create_card_for_board(board_id):
#     validate_model(Board, board_id)  
#     response_data, status_code = create_class_instance(Card, request, ["message", "owner"], {"board_id": board_id})
#     send_card_created_message(response_data["card"]["message"])
#     return response_data, status_code

@bp.patch('/<card_id>')
def update_card(card_id):
    return update_instance(Card, card_id, request)


@bp.delete("/<card_id>", strict_slashes=False)
def delete_card(card_id):
    return delete_instance(Card, card_id)


@bp.patch('/like/<card_id>')
def increment_likes(card_id):
    return update_instance(Card, card_id, request, like=True)
