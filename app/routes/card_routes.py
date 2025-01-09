from flask import Blueprint, request
from app.routes.route_utilities import *
from app.models.card import Card
from app.models.board import Board

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")


@bp.get('/<card_id>')
def get_one_card(card_id):
    return get_one_instance(Card, card_id)


@bp.patch('/<card_id>')
def update_card(card_id):
    return update_instance(Card, card_id, request)


@bp.delete("/<card_id>", strict_slashes=False)
def delete_card(card_id):
    return delete_instance(Card, card_id)


@bp.patch('/like/<card_id>')
def increment_likes(card_id):
    return update_instance(Card, card_id, request, like=True)

