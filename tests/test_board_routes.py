from app.models.board import Board
import pytest


# READ/boards
# @pytest.mark.skip
def test_all_boards_empty_database(client):
    # Act
    response = client.get('/boards/')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip
def test_get_all_boards_in_database(client, multiple_boards):
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
    # Act
    responese = client.get('/boards/?invalid_param=something')
    responese_body = responese.get_json()

    # Assert
    assert responese.status_code == 200
    assert len(responese_body) == 3

    assert responese_body[0]["title"] == "Board 1"
    assert responese_body[1]["title"] == "Board 2"
    assert responese_body[2]["title"] == "Board 3"


# @pytest.mark.skip
def test_get_one_particular_board_success(client, sample_board):
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
    # Act
    responese = client.get('/boards/999')
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


# @pytest.mark.skip
def test_create_board_missing_field_required(client):
    # Arrange
    request_body = {
        "title": "New Test Board"
        # missing owner
    }
    # Act
    response = client.post('/boards/', json=request_body)
    response_body = response.get_json()
    print(f"Response Body: {response_body}")

    # Assert
    assert response.status_code == 400
    assert "Invalid request: missing owner" in response_body["details"]



# UPDATE/boards
'''' need to check on board to see if there is a patch or put... patch is for update'''

# @pytest.mark.skip
def test_update_board_sucessful(client, sample_board):
    # Arrange
    update_data = {
        "title": "Updated Title",
        "owner": "new_owner"
    }
    # Act
    response = client.put(f'/boards/{sample_board.id}', json=update_data)
    response_body = response.get_json()
    print(f"response body: {response_body}")

    # Assert
    assert response.status_code == 200
    assert response_body["board"]["title"] == "Updated Title"
    assert response_body["board"]["owner"] == "new_owner"

    # verify changes were saved
    verify_response = client.get(f'/boards/{sample_board.id}')
    verify_body = verify_response.get_json()
    assert verify_body["board"]["title"] == "Updated Title"
    assert verify_body["board"]["owner"] == "new_owner"


# @pytest.mark.skip
def test_updated_board_not_found(client):
    # Arrange
    update_data = {
        "title": "New Title",
        "owner": "new_owner"
    }

    # Act
    responese = client.put('/boards/999', json=update_data)
    responese_body = responese.get_json()
    print(f"response body: {responese_body}")

    # Assert
    assert responese.status_code == 404
    assert "was not found" in responese_body["message"]

    # verify
    verify_response = client.get('/boards/999')
    assert verify_response.status_code == 404


# @pytest.mark.skip
def test_update_board_invalid_data(client, sample_board):
    # Act
    response = client.put(f'/boards/{sample_board}', json={})
    response_body = response.get_json()
    print(f"response body: {response_body}")
    # Assert

    assert response.status_code == 400
    assert "details" f"Board {sample_board} is invalid"


@pytest.mark.skip
# This test should not return 400 as we use PATCH (not PUT)
# which means that the title stays intact if we update only thw owner
def test_update_board_with_missing_title(client, sample_board):
    # Act
    response = client.put(
        f'/boards/{sample_board.id}', json={"owner": "new_owner"})
    response_body = response.get_json()
    # print(f'response body: {response_body}')

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "Title is required"


@pytest.mark.skip
# This test should not return 400 as we use PATCH (not PUT)
# which means that the owner stays intact if we update only title
def test_update_board_with_missing_owner(client, sample_board):
    # Act
    response = client.put(
        f"/boards/{sample_board.id}", json={"title": "New Title"})
    response_body = response.get_json()
    print(f"response body: {response_body}")

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "Owner is required"


# DELETE/boards
# @pytest.mark.skip
def test_delete_board_is_sucessful(client, sample_board):
    # Act
    response = client.delete(f'/boards/{sample_board.id}')
    response_body = response.get_json()
    print(f"Response Body: {response_body}")

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "details": f"Board {sample_board.id} successfully deleted"
    }

    # verify board is really deleted
    verify_response = client.get(f'/boards/{sample_board.id}')
    assert verify_response.status_code == 404


# @pytest.mark.skip
def test_delete_board_not_found(client):
    # Act
    responese = client.delete('/boards/999')
    responese_body = responese.get_json()
    print(f"response body: {responese_body}")

    # Assert
    assert responese.status_code == 404
    assert "was not found" in responese_body["message"]

    # verify
    verify_response = client.delete('/boards/999')
    verify_body = verify_response.get_json()
    assert "was not found" in verify_body["message"]


# READ boards/<id>/cards
# @pytest.mark.skip
def test_get_card_from_board_success(client, sample_board, sample_card):
    # Act
    response = client.get(f'/boards/{sample_board.id}/cards')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["cards"][0]["message"] == "Test Card"


# @pytest.mark.skip
def test_board_exist_but_has_no_card(client, sample_board):
    response = client.get(f'/boards/{sample_board.id}/cards')
    response_body = response.get_json()
    print(f"response body: {response_body}")

    # Assert
    assert response.status_code == 200
    assert response_body["cards"] == []


# @pytest.mark.skip
def test_get_card_from_non_existing_board(client):
    # Act
    response = client.get(f'/boards/999/cards')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "was not found" in response_body["message"]


# CREATE/boards/<id>/cards
# @pytest.mark.skip
def test_create_card_for_board_success(client, sample_board):
    # Arrange
    board_id = sample_board.id
    new_card_data = {
        "message": "Test Card",
        "owner": "test_owner"
    }
    # Act
    response = client.post(
        f"/boards/{sample_board.id}/cards", json=new_card_data)
    response_body = response.get_json()["card"]
    print(f"response body: {response_body}")
    # Assert
    assert response.status_code == 201
    assert response_body["message"] == "Test Card"
    assert response_body["owner"] == "test_owner"
    assert response_body["board_id"] == board_id


# @pytest.mark.skip
def test_create_card_for_nonexistent_board(client):
    # Arrange
    new_card_data = {
        "message": "New Test Card",
        "owner": "test_owner"
    }

    # Act
    response = client. post("/boards/999/cards", json=new_card_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "not found" in response_body["message"].lower()


# @pytest.mark.skip
def test_create_card_missing_message(client, sample_board):

    # Act
    response = client.post(
        f"/boards/{sample_board.id}/cards", json={"owner": "test_owner"})
    response_body = response.get_json()
    print(f'response body: {response_body}')
    # Assert
    assert response.status_code == 400
    assert "missing message" in response_body["details"].lower()
