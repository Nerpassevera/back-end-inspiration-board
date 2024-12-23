import pytest
from app import create_app  
from app.db import db
from flask.signals import request_finished
from app.models.card import Card
from app.models.board import Board

@pytest.fixture
def app():
  test_config ={
    "TESTING": True,
    # "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI'),
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"  
    
  }
  app = create_app(test_config)
  
  @request_finished.connect_via(app)
  def expire_session(sender, response, **extra):
    db.session.remove()
    
  with app.app_context():
    db.create_all()
    yield app
    
  with app.app_context():
    db.drop_all()
    
@pytest.fixture
def client(app):
  return app.test_client()

# In your conftest.py, add these fixtures:

@pytest.fixture
def sample_board(app):
    with app.app_context():
        board = Board(
          title="Test Board",
          owner="test_owner"
          )
        db.session.add(board)
        db.session.commit()
        yield board
        # Cleanup
        db.session.delete(board)
        db.session.commit()

@pytest.fixture
def sample_card(app, sample_board):
    with app.app_context():
        card = Card(
            message="Test Card",
            likes_count=2,
            board_id=sample_board.id
        )
        db.session.add(card)
        db.session.commit()
        yield card
        # Cleanup
        db.session.delete(card)
        db.session.commit()

# test_setup.py or you can add these to either test file
def test_database_setup(app):
    # This test verifies that your app fixture is working
    assert app.config['TESTING'] is True
    assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']

def test_client_setup(client):
    # This tests that your client fixture works
    response = client.get('/')  # or any valid endpoint
    assert response is not None

def test_sample_board_fixture(sample_board):
    # This tests that your board fixture creates records correctly
    assert sample_board.id is not None
    assert sample_board.title == "Test Board"

def test_sample_card_fixture(sample_card, sample_board):
    # This tests that your card fixture works and properly relates to board
    assert sample_card.id is not None
    assert sample_card.board_id == sample_board.id
    assert sample_card.message == "Test Card"