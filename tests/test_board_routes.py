from app.models.board import Board
import pytest

# @pytest.mark.skip
def test_all_boards_empty(client):
  '''Test getting all board when database is empyt '''
  # Act
  response = client.get('/boards/')
  response_body = response.get_json()
  
  # Assert
  assert response.status_code == 200
  assert response_body == []

# @pytest.mark.skip
def test_get_all_boards(client, multiple_boards):
  ''' Test getting all boards wieh there are boards in the db'''
  # Act
  response = client.get('/boards/')
  response_body = response.get_json()
  
  # Assert 
  assert response.status_code == 200
  assert len(response_body) == 3
  
  assert response_body[0]["title"] == "Board 1"
  assert response_body[1]["title"] == "Board 2"
  assert response_body[2]["title"] == "Board 3"

# @pytest.mark.skip
def test_get_all_boards_with_invalid_query(client, multiple_boards):
  ''' Test getting all boards with invaild queery param'''
  # Act
  responese = client.get('/boards/?invalid_param=something')
  responese_body = responese.get_json()

  # Assert
  assert responese.status_code == 200
  assert len(responese_body)== 3

  assert responese_body[0]["title"] == "Board 1"
  assert responese_body[1]["title"] == "Board 2"
  assert responese_body[2]["title"] == "Board 3"
  

# @pytest.mark.skip
def test_get_one_board_success(client, sample_board):
  ''' Sucessed, get a specific board'''
  # Act
  responese = client.get(f'/boards/{sample_board.id}')
  responese_body = responese.get_json()

  # Assert
  assert responese.status_code == 200
  assert responese_body["board"]["title"] == "Test Board"
  assert responese_body["board"]["owner"] == "test_owner"
  assert responese_body["board"]["id"] == sample_board.id

  # @pytest.mark.skip
def test_get_one_board_not_found(client):
  ''' Board does not exits'''
  # Act
  responese =client.get('/boards/999')
  responese_body = responese.get_json()
  print(f"response body: {responese_body}")
  
  # Assert
  assert responese.status_code == 404
  assert "was not found" in responese_body["message"]
  
# create a board
# @pytest.mark.skip
def test_create_board_success(client):
  # Arrange
  request_body = {
    "title": "New Test Board",
    "owner": "test_owner"
  }
  
  # Act
  response = client.post('/boards/', json=request_body)
  response_body = response.get_json()
  # Assert
  assert response.status_code == 201 
  assert response_body["board"]["title"] == "New Test Board"
  assert response_body["board"]["owner"] == "test_owner"
  
#missing data
def test_create_board_missing_field(client):
    '''Test creating a board with missing required field'''
    



# 2. delete_board tests
#     - Success case
#     - Not found case

# 3. update_board tests
#     - Success case
#     - Not found case
#     - Invalid data case

# 4. board_cards tests
#     - Success case
#     - Empty cards case
#     - Not found case