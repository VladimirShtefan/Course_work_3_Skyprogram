from app.blueprints.post_blueprint.dao.post_dao import Post, User, File
from app.paths import DATA_JSON_PATH, COMMENTS_JSON_PATH

import pytest


@pytest.fixture()
def post_dao():
    post_dao_instance = Post(DATA_JSON_PATH, COMMENTS_JSON_PATH)
    return post_dao_instance


@pytest.fixture()
def file_dao():
    file_dao_instance = File(DATA_JSON_PATH, COMMENTS_JSON_PATH)
    return file_dao_instance


class TestFileDao:
    def test_get_all_posts(self, file_dao):
        posts = file_dao.get_all_posts()
        assert type(posts) == list, 'вернулся не список с постами'
        assert type(posts[0]) == dict, 'в списке не верный тип данных постов'
        assert len(posts) > 0, 'вернулся пустой список с постами'
        assert list(posts[0].keys()) == ["poster_name",
                                         "poster_avatar",
                                         "pic",
                                         "content",
                                         "views_count",
                                         "likes_count",
                                         "pk"
                                         ], 'не совпадают ключи у словаря с постами'

    def test_get_all_comments(self, file_dao):
        comments = file_dao.get_all_comments()
        assert type(comments) == list, 'вернулся не список с комментариями'
        assert type(comments[0]) == dict, 'в списке не верный тип данных комментариев'
        assert len(comments) > 0, 'вернулся пустой список с комментариями'
        assert list(comments[0].keys()) == ["post_id",
                                            "commenter_name",
                                            "comment",
                                            "pk"
                                            ], 'не совпадают ключи в комментариях'


class TestPostDao:
    def test_get_number_comments_with_post_id(self, post_dao):
        dict_number_comments = post_dao.get_number_comments_with_post_id()
        assert type(dict_number_comments) == dict, 'не верный тип данных'

    def test_get_post_for_pk(self, post_dao):
        post = post_dao.get_post_for_pk(1)
        assert type(post) == dict, 'не верный формат поста'
        assert list(post.keys()) == ["poster_name",
                                     "poster_avatar",
                                     "pic",
                                     "content",
                                     "views_count",
                                     "likes_count",
                                     "pk"
                                     ], 'не совпадают ключи у словаря с постами'

    def test_get_comments_for_post_by_pk(self, post_dao):
        comments = post_dao.get_comments_for_post_by_pk(1)
        assert type(comments) == list, 'вернулся не список с комментариями'
        assert type(comments[0]) == dict, 'в списке не верный тип данных комментариев'
        assert len(comments) > 0, 'вернулся пустой список с комментариями'
        assert list(comments[0].keys()) == ["post_id",
                                            "commenter_name",
                                            "comment",
                                            "pk"
                                            ], 'не совпадают ключи в комментариях'

    def test_search_posts(self, post_dao):
        posts = post_dao.search_posts('')
        assert type(posts) == list, 'вернулся не список с постами'
        assert type(posts[0]) == dict, 'в списке не верный тип данных постов'
        assert len(posts) > 0, 'вернулся пустой список с постами'
        assert list(posts[0].keys()) == ["poster_name",
                                         "poster_avatar",
                                         "pic",
                                         "content",
                                         "views_count",
                                         "likes_count",
                                         "pk"
                                         ], 'не совпадают ключи у словаря с постами'
