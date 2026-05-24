import pytest

from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController

@pytest.fixture
def sut():
    mock_dao = MagicMock()
    controller = UserController(dao=mock_dao)

    return controller, mock_dao

def test_get_user_by_email_single_result(sut):
    controller, mock_dao = sut
    mock_dao.find.return_value = [{"email": "test@example.com", "name": "Alice"}]
    result = controller.get_user_by_email("test@example.com")
    assert result == {"email": "test@example.com", "name": "Alice"}
def test_get_user_by_email_no_result(sut):
    controller, mock_dao = sut
    mock_dao.find.return_value = []
    result = controller.get_user_by_email("nobody@example.com")
    assert result is None


def test_get_user_by_email_multiple_results(sut):
    controller, mock_dao = sut

    user1 = {"email": "dup@example.com", "name": "Alice"}
    user2 = {"email": "dup@example.com", "name": "Bob"}
    mock_dao.find.return_value = [user1, user2]

    result = controller.get_user_by_email("dup@example.com")
    assert result == user1
def test_get_user_by_email_invalid_email(sut):
    controller, mock_dao = sut
    with pytest.raises(ValueError):
        controller.get_user_by_email("notanemail")
    mock_dao.find.assert_not_called()

def test_get_user_by_email_empty_string(sut):
    controller, mock_dao = sut

    with pytest.raises(ValueError):
        controller.get_user_by_email("")

    mock_dao.find.assert_not_called()


def test_get_user_by_email_forwards_dao_exception(sut):
    controller, mock_dao = sut
    mock_dao.find.side_effect = RuntimeError("database unavailable")
    with pytest.raises(RuntimeError):
        controller.get_user_by_email("test@example.com")
