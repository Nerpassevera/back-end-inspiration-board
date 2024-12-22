from flask import Blueprint, request
from os import environ

from app.models.card import Card
from app.db import db
from app.routes.route_utilities import *

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@bp.post("/", strict_slashes=False)
def create_card():
    return create_class_instance(Card, request, ["title", "description"])
