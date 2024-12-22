from flask import Blueprint, request
from app.routes.route_utilities import create_class_instance, get_all_instances, get_one_instance, delete_instance, update_instance, validate_model
from app.models.card import Card

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")


@bp.get('/')
def get_all_cards():
    return get_all_instances(Card, request.args)

@bp.get('/<card_id>')
def get_one_card(card_id):
    return get_one_instance(Card, card_id)

@bp.patch('/<card_id>')
def update_card(card_id):
    return update_instance(Card, card_id, request)