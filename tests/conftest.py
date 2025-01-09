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

# fixtures for test_setup

@pytest.fixture
def sample_board(app):
    """Fixture for a single board - can be used across all test files"""
    with app.app_context():
        board = Board(
            title="Test Board",
            owner="test_owner"
        )
        db.session.add(board)
        db.session.commit()
        
        yield board
        
        # Cleanup
        try:
            db.session.query(Board).filter_by(id=board.id).delete()
            db.session.commit()
        except:
            db.session.rollback()

@pytest.fixture
def sample_card(app, sample_board):
    with app.app_context():
        card = Card(
            message="Test Card",
            likes_count=2,
            board_id=sample_board.id,
            owner="test_owner"
        )
        db.session.add(card)
        db.session.commit()
        yield card
        # Cleanup
        db.session.delete(card)
        db.session.commit()
   
# fixture for board_routes
# test  board creation 
# @pytest.fixture
# def sample_board(app):
#   ''' Single board fixture for test'''
#   with app.app_context():
#     board = Board(
#       title="Test Board",
#       owner="test_owner"
#       )
#     db.session.add(board)
#     db.session.commit()
#     yield board
    
#     try:
#       db.session.query(Board).filter_by(id=board.id).delete()
#       db.session.commit()
#     except:
#       db.session.rollback()
      
@pytest.fixture
def multiple_boards(app):
  """fixture creating multiple boards for list/collection test"""
  with app.app_context():
    boards =[
      Board(
        title="Board 1", owner="owner1"
      ),
      Board(
        title="Board 2", owner="owner2"
      ),
      Board(
        title="Board 3", owner="owner3"
      )
    ]  
    for board in boards:
      db.session.add(board)
    db.session.commit()
    yield boards
    
    for board in boards:
      db.session.delete(board)
    db.session.commit()
    
@pytest.fixture
def multiple_cards(app, sample_board):
  """fixture creating multiple cards for collection/list test"""
  with app.app_context():
      cards = [
          Card(
              message="Test Card 1",
              likes_count=0,
              board_id=sample_board.id,
              owner="test_owner1"
          ),
          Card(
              message="Test Card 2",
              likes_count=5,
              board_id=sample_board.id,
              owner="test_owner2"
          ),
          Card(
              message="Test Card 3",
              likes_count=10,
              board_id=sample_board.id,
              owner="test_owner3"
          )
      ]
      for card in cards:
          db.session.add(card)
      db.session.commit()
      yield cards
      
      for card in cards:
          db.session.delete(card)
      db.session.commit()
