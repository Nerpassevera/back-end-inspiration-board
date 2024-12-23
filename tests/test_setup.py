# tests/test_setup.py
from app.models.board import Board
from app.models.card import Card

def test_database_setup(app):
    assert app.config['TESTING'] is True
    assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']

def test_client_setup(client):
    response = client.get('/boards')  # assuming you have a /boards endpoint
    assert response is not None

def test_sample_board_fixture(sample_board):
    assert sample_board.id is not None
    assert sample_board.title == "Test Board"

def test_sample_card_fixture(sample_card, sample_board):
    assert sample_card.id is not None
    assert sample_card.board_id == sample_board.id
    assert sample_card.message == "Test Card"