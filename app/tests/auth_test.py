import pytest

from app.blueprints.auth import UserDetect
from app.exceptions import FileCommentsNotExists, NotExpectedType
from app.paths import USERS_JSON_PATH


@pytest.fixture()
def user_detect():
    user = UserDetect({'User-Agent': 'test'}, '127.0.0.1', USERS_JSON_PATH)
    return user


@pytest.fixture()
def break_user_detect():
    break_user = UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test.json')
    return break_user


@pytest.fixture()
def break_users_file_bad_content():
    break_user = UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'app/tests/test_users_bad_content.json')
    return break_user


class TestAuth:
    def test_get_md5_for_user(self, user_detect):
        assert isinstance(user_detect.get_md5_for_user(), str), 'не верный тип данных в md5'
        assert len(user_detect.get_md5_for_user()) == 32, 'длина не соответствует md5'

    def test_load_users(self, user_detect, break_user_detect, break_users_file_bad_content):
        assert isinstance(user_detect.load_users(), list), 'не верный тип возвращаемых данных'

        with pytest.raises(FileCommentsNotExists) as exception_err:
            break_user_detect.load_users()
        exception_message = exception_err.value.message
        assert exception_message == 'Фаил c комментариями не найден', 'не верно работает исключение по файлу с users'

        with pytest.raises(NotExpectedType) as exception_err:
            break_users_file_bad_content.load_users()
        exception_message = exception_err.value.message
        assert exception_message == 'Не верный формат данных', 'не верно работает исключение по содержимому файла с ' \
                                                               'users '

    def test_get_all_users_md5(self, user_detect):
        assert isinstance(user_detect.get_all_users_md5(), list), 'не верный тип возвращаемых данных'

    # def test_get_like(self, users_file):
    #     assert users_file.get_like(1) == False



# @mock.patch('app.blueprints.auth.UserDetect.load_users')
# def test_load_users_type(mock_load_users: mock.Mock, user_detect):
#     mock_load_users.return_value = 5
#     assert user_detect.load_users() == 5
