import json
from unittest.mock import mock_open, patch

import pytest

from app.blueprints.auth import UserDetect
from app.exceptions import FileCommentsNotExists, NotExpectedType


class TestAuth:

    def test_get_md5_for_user(self):
        assert isinstance(UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').get_md5_for_user(), str)

    def test_load_users(self, open_mock):
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').load_users() == [{'post_id': 1}]
        open_mock.side_effect = FileNotFoundError
        with pytest.raises(FileCommentsNotExists):
            UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').load_users()

    @pytest.mark.parametrize('data', {'id': 1, 'name': 'ivan'})
    def test_load_users_2(self, data):
        with pytest.raises(NotExpectedType):
            with patch('builtins.open', new_callable=mock_open, read_data=json.dumps(data)):
                UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').load_users()

    def test_write_user(self, open_mock):
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').write_user([{'post_id': 2}]) is None

    @patch('app.blueprints.auth.UserDetect.load_users', return_value=[{"user_md5": "cca173be1c70b68f7852b7aaf8a27f93"}])
    def test_get_all_users_md5(self, load_users):
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').get_all_users_md5() == ["cca173be1c70b68f"
                                                                                               "7852b7aaf8a27f93"]

    @patch('app.blueprints.auth.UserDetect.get_md5_for_user', return_value="cca173be1c70b68f7852b7aaf8a27f93")
    @patch('app.blueprints.auth.UserDetect.get_all_users_md5', return_value=["cca173be1c70b68f7852b7aaf8a27f93"])
    @patch('app.blueprints.auth.UserDetect.load_users', return_value=[{"user_md5": "cca173be1c70b68f7852b7aaf8a27f93",
                                                                       "pk_posts_with_like": [],
                                                                       "pk_posts_in_bookmarks": [],
                                                                       }])
    def test_add_new_user(self, load_users, get_md5_for_user, get_all_users_md5, open_mock):
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').add_new_user() is None
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').get_like(1) is True
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').get_bookmark(1) is True

    @patch('app.blueprints.auth.UserDetect.get_md5_for_user', return_value="gfhjbnk")
    @patch('app.blueprints.auth.UserDetect.get_all_users_md5', return_value=["cca173be1c70b68f7852b7aaf8a27f93"])
    @patch('app.blueprints.auth.UserDetect.load_users', return_value=[{"user_md5": "cca173be1c70b68f7852b7aaf8a27f93",
                                                                       "pk_posts_with_like": [1],
                                                                       "pk_posts_in_bookmarks": [1],
                                                                       }])
    def test_add_new_user_2(self, load_users, get_md5_for_user, get_all_users_md5, open_mock):
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').add_new_user() is None

    @patch('app.blueprints.auth.UserDetect.get_md5_for_user', return_value="cca173be1c70b68f7852b7aaf8a27f93")
    @patch('app.blueprints.auth.UserDetect.load_users', return_value=[{"user_md5": "cca173be1c70b68f7852b7aaf8a27f93",
                                                                       "pk_posts_with_like": [1],
                                                                       "pk_posts_in_bookmarks": [1],
                                                                       }])
    def test_add_new_user_3(self, load_users, get_md5_for_user, open_mock):
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').get_like(1) is False
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').get_bookmark(1) is False

    @patch('app.blueprints.auth.UserDetect.get_md5_for_user', return_value="gfhjbnk")
    @patch('app.blueprints.auth.UserDetect.load_users', return_value=[{"user_md5": "cca173be1c70b68f7852b7aaf8a27f93",
                                                                       "pk_posts_with_like": [1],
                                                                       "pk_posts_in_bookmarks": [1],
                                                                       }])
    def test_add_new_user_4(self, load_users, get_md5_for_user):
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').get_like(1) is None
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').get_bookmark(1) is None

    @patch('app.blueprints.auth.UserDetect.get_all_users_md5', return_value=["cca173be1c70b68f7852b7aaf8a27f93"])
    @patch('app.blueprints.auth.UserDetect.get_md5_for_user', return_value="cca173be1c70b68f7852b7aaf8a27f93")
    @patch('app.blueprints.auth.UserDetect.load_users', return_value=[{"user_md5": "cca173be1c70b68f7852b7aaf8a27f93",
                                                                       "pk_posts_with_like": [1],
                                                                       "pk_posts_in_bookmarks": [1],
                                                                       }])
    def test_get_likes_list(self, load_users, get_md5_for_user, get_all_users_md5):
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').get_likes_list() == [1]
        assert UserDetect({'User-Agent': 'test'}, '127.0.0.1', 'test').get_bookmarks_list() == [1]
