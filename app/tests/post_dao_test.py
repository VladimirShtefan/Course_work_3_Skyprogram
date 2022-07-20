import json
from unittest.mock import patch, mock_open

from app.blueprints.post_blueprint.dao.post_dao import File, Post
from app.exceptions import FilePostsNotExists, NotExpectedType, FileCommentsNotExists, DictKeyNotFoundError, \
    PageNotFoundError

import pytest


class TestFileDao:

    def test_get_all_posts(self, open_mock):
        assert File('text.json', 'text.json').get_all_posts() == [{'post_id': 1}]
        open_mock.side_effect = FileNotFoundError
        with pytest.raises(FilePostsNotExists):
            File('text.json', 'text.json').get_all_posts()

    @pytest.mark.parametrize('data', {'id': 1, 'name': 'ivan'})
    def test_isinstance_get_all_posts_and_comments(self, data):
        with pytest.raises(NotExpectedType):
            with patch('builtins.open', new_callable=mock_open, read_data=json.dumps(data)):
                File('text.json', 'text.json').get_all_posts()
        with pytest.raises(NotExpectedType):
            with patch('builtins.open', new_callable=mock_open, read_data=json.dumps(data)):
                File('text.json', 'text.json').get_all_comments()

    def test_get_all_comments(self, open_mock):
        assert File('text.json', 'text.json').get_all_comments() == [{'post_id': 1}]
        open_mock.side_effect = FileNotFoundError
        with pytest.raises(FileCommentsNotExists):
            File('text.json', 'text.json').get_all_comments()

    def test_write_comments(self, open_mock):
        assert File('text.json', 'text.json').write_comments([{'post_id': 2}]) is None

    def test_update_posts(self, open_mock):
        assert File('text.json', 'text.json').update_posts([{'post_id': 2}]) is None


class TestPostDao:

    def test_get_number_comments_with_post_id(self, open_mock):
        assert Post('text.json', 'text.json').get_number_comments_with_post_id() == {1: 1}

    @patch('app.blueprints.storage.File.get_all_comments', return_value=[{'post_id': 1}, {'post_id': 1}])
    def test_get_number_comments_with_post_id_2(self, get_all_comments, open_mock):
        assert Post('text.json', 'text.json').get_number_comments_with_post_id() == {1: 2}

    @patch('app.blueprints.storage.File.get_all_comments', return_value=[{'id': 1}, {'id': 1}])
    def test_get_number_comments_with_post_id_3(self, get_all_comments):
        with pytest.raises(DictKeyNotFoundError):
            Post('text.json', 'text.json').get_number_comments_with_post_id()

    @patch('app.blueprints.storage.File.get_all_posts', return_value=[{'id': 1}, {'id': 1}])
    def test_get_post_for_pk(self, get_all_posts):
        with pytest.raises(DictKeyNotFoundError):
            Post('text.json', 'text.json').get_post_for_pk(1)

    @patch('app.blueprints.storage.File.get_all_posts', return_value=[{"content": "#test", "pk": 2}])
    def test_get_post_for_pk_1(self, get_all_posts):
        assert Post('text.json', 'text.json').get_post_for_pk(2) == [{"content": '<a href="/tag/test">#test</a>',
                                                                      "pk": 2}]
        with pytest.raises(PageNotFoundError):
            Post('text.json', 'text.json').get_post_for_pk(1)

    @patch('app.blueprints.storage.File.get_all_posts', return_value=[{"content": "#test", "pk": 2}])
    def test_get_bookmark_posts(self, get_all_posts):
        assert Post('text.json', 'text.json').get_bookmark_posts([2]) == [{"content": "#test", "pk": 2}]

    @patch('app.blueprints.storage.File.get_all_comments', return_value=[{'post_id': 1}, {'post_id': 1}])
    def test_get_comments_for_post_by_pk(self, get_all_comments):
        assert Post('text.json', 'text.json').get_comments_for_post_by_pk(1) == [{'post_id': 1}, {'post_id': 1}]

    @patch('app.blueprints.storage.File.get_all_posts', return_value=[{"content": "#test", "pk": 2}])
    def test_search_posts(self, get_all_posts):
        assert Post('text.json', 'text.json').search_posts('test') == [{"content": "#test", "pk": 2}]

    @patch('app.blueprints.storage.File.get_all_posts', return_value=[{"content": "#test", "pk": 2}])
    def test_add_new_comment(self, get_all_posts, open_mock):
        assert Post('text.json', 'text.json').add_new_comment('name', 'comment', 3) is None

    @patch('app.blueprints.storage.File.get_all_posts', return_value=[{"pk": 2, "likes_count": 103}])
    def test_update_likes_post(self, get_all_posts, open_mock):
        assert Post('text.json', 'text.json').update_likes_post(2, 'like') == 104

    @patch('app.blueprints.storage.File.get_all_posts', return_value=[{"pk": 2, "likes_count": 103}])
    def test_update_likes_post_2(self, get_all_posts, open_mock):
        assert Post('text.json', 'text.json').update_likes_post(2, 'dislike') == 102

    @patch('app.blueprints.storage.File.get_all_posts', return_value=[{"pk": 2, "likes_count": 103}])
    def test_update_likes_post_3(self, get_all_posts, open_mock):
        assert Post('text.json', 'text.json').update_likes_post(2) == 103

    @patch('app.blueprints.storage.File.get_all_posts', return_value=[{"pk": 2, "views_count": 249}])
    def test_update_views_post(self, get_all_posts, open_mock):
        assert Post('text.json', 'text.json').update_views_post(2) is None

    @patch('app.blueprints.storage.File.get_all_posts', return_value=[{"pk": 2, "poster_name": "johnny"}])
    def test_get_all_post_by_user_name(self, get_all_posts):
        assert Post('text.json', 'text.json').get_all_post_by_user_name('johnny') == [{"pk": 2,
                                                                                       "poster_name": "johnny"}]
