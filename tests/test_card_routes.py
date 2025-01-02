import pytest


# READ/cards
# @pytest.mark.skip
def test_get_one_particular_card_success(client, sample_card):
    # Act
    responese = client.get(f'/cards/{sample_card.id}')
    responese_body = responese.get_json()

    # Assert
    assert responese.status_code == 200
    assert responese_body["card"]["message"] == "Test Card"
    assert responese_body["card"]["owner"] == "test_owner"
    assert responese_body["card"]["id"] == sample_card.id


# @pytest.mark.skip
def test_get_one_carrd_not_found(client):
    # Act
    responese = client.get('/cards/999')
    responese_body = responese.get_json()
    print(f"response body: {responese_body}")

    # Assert
    assert responese.status_code == 404
    assert "was not found" in responese_body["message"]


# create a card
# @pytest.mark.skip
def test_create_card_success(client, sample_board):
    # Arrange
    request_body = {
        "message": "New Test Card",
        "owner": "test_owner"
    }

    # Act
    with client.application.app_context():
        response = client.post(
            f'/boards/{sample_board.id}/cards', json=request_body)
        response_body = response.get_json()["card"]
        print(f"Response Body: {response_body}")

        # Assert
        assert response.status_code == 201
        assert response_body["message"] == "New Test Card"
        assert response_body["owner"] == "test_owner"
        assert response_body["board_id"] == sample_board.id


# @pytest.mark.skip
def test_create_card_missing_field_required(client, sample_board):
    # Arrange
    request_body = {
        "message": "New Test Card"
    }
    # Act
    with client.application.app_context():
        response = client.post(
            f'/boards/{sample_board.id}/cards', json=request_body)
        response_body = response.get_json()
        print(f"Response Body: {response_body}")

        # Assert
        assert response.status_code == 400
        assert "Invalid request: missing owner" in response_body["details"]


# @pytest.mark.skip
def test_update_card_success(client, sample_card):
    # Arrange
    update_data = {
        "message": "Updated Message",
        "owner": "new_owner"
    }

    # Act
    with client.application.app_context():
        response = client.patch(f'/cards/{sample_card.id}', json=update_data)
        response_body = response.get_json()

        # Assert
        assert response.status_code == 200
        assert response_body["card"]["message"] == "Updated Message"
        assert response_body["card"]["owner"] == "new_owner"


def test_update_card_not_found(client):
    with client.application.app_context():
        response = client.patch('/cards/999', json={"message": "Test"})
        assert response.status_code == 404


# Delete/ cards
# @pytest.mark.skip
def test_delete_card_success(client, sample_card):
    # Act
    with client.application.app_context():
        response = client.delete(f'/cards/{sample_card.id}')
        response_body = response.get_json()

        # Assert
        assert response.status_code == 200
        assert "successfully deleted" in response_body["details"]

        # Verify card is deleted
        verify_response = client.get(f'/cards/{sample_card.id}')
        assert verify_response.status_code == 404


# @pytest.mark.skip
def test_delete_card_not_found(client):
    with client.application.app_context():
        response = client.delete('/cards/999')
        assert response.status_code == 404


# like increment test
# @pytest.mark.skip
def test_increment_likes_success(client, sample_card):
    # Act
    with client.application.app_context():
        response = client.patch(f'/cards/like/{sample_card.id}', json={})
        response_body = response.get_json()

        # Assert
        assert response.status_code == 200
        assert response_body["card"]["likes_count"] == 3


def test_increment_likes_not_found(client):
    with client.application.app_context():
        response = client.patch('/cards/like/999', json={})
        assert response.status_code == 404
