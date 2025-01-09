from flask import Blueprint, Response

bp = Blueprint("meta_bp", __name__, url_prefix="/")

@bp.get("/")
def welcome_message():
    """
    Returns information about the API and its available endpoints.
    """
    message = (
        "Welcome to the Inspiration Board API!\n\n"
        "Description: A RESTful API for managing inspiration boards and cards.\n\n"
        "Available Endpoints:\n\n"
        "Boards:\n"
        "  GET    /boards         - Retrieve all boards\n"
        "  POST   /boards         - Create a new board\n"
        "  GET    /boards/<id>    - Retrieve a specific board\n"
        "  PUT    /boards/<id>    - Update a specific board\n"
        "  DELETE /boards/<id>    - Delete a specific board\n\n"
        "Cards:\n"
        "  GET    /boards/<board_id>/cards - Retrieve all cards for a board\n"
        "  POST   /boards/<board_id>/cards - Add a new card to a specific board\n"
        "  GET    /cards/<card_id>         - Retrieve a specific card\n"
        "  PATCH  /cards/<card_id>         - Update a specific card\n"
        "  DELETE /cards/<card_id>         - Delete a specific card\n"
        "  PATCH  /cards/like/<card_id>    - Increment like count for a card\n\n"
        "Deployment URL: https://front-end-inspiration-board.onrender.com/"
    )
    return Response(message, content_type="text/plain")
