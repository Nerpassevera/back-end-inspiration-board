from flask import Flask
from flask_cors import CORS
import os

from .routes.board_routes import bp as board_bp
from .routes.card_routes import bp as card_bp
from .routes.meta_rutes import bp as meta_bp
from .db import db, migrate
from .models.board import Board
from .models.card import Card
# Import models, blueprints, and anything else needed to set up the app or database


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')


    if config:
        app.config.update(config)

    # Initialize app with SQLAlchemy db and Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints 
    app.register_blueprint(board_bp)
    app.register_blueprint(card_bp)
    app.register_blueprint(meta_bp)


    CORS(app)
    return app

if __name__ == '__main__':
    inspiration_board_app = create_app()