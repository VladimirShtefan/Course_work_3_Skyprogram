import json

from app.blueprints.post_blueprint.dao.post_dao import Post, File
from app.exceptions import DictKeyNotFoundError, PageNotFoundError, FilePostsNotExists, NotExpectedType, \
    FileCommentsNotExists
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


@pytest.fixture()
def file_dao_bad_content():
    file_dao_break = Post('app/tests/test_bad_json.json', 'app/tests/test_bad_json.json')
    return file_dao_break


@pytest.fixture()
def file_dao_test_posts():
    file_dao_posts = Post('app/tests/test_posts.json', 'app/tests/test_posts.json')
    return file_dao_posts


@pytest.fixture()
def file_dao_test_comments():
    file_dao_comments = Post('app/tests/test_file_with_comments.json', 'app/tests/test_file_with_comments.json')
    return file_dao_comments


@pytest.fixture()
def post_file_bad_json():
    bad_json = File('app/tests/test_users_bad_content.json', 'app/tests/test_users_bad_content.json')
    return bad_json


@pytest.fixture()
def break_post_file():
    break_posts_file = File('test.json', 'test.json')
    return break_posts_file


class TestFileDao:
    def test_get_all_posts(self, file_dao, break_post_file, post_file_bad_json):
        posts = file_dao.get_all_posts()
        assert isinstance(posts, list), 'вернулся не список с постами'
        assert isinstance(posts[0], dict), 'в списке не верный тип данных постов'
        assert len(posts) > 0, 'вернулся пустой список с постами'
        assert list(posts[0].keys()) == ["poster_name",
                                         "poster_avatar",
                                         "pic",
                                         "content",
                                         "views_count",
                                         "likes_count",
                                         "pk"
                                         ], 'не совпадают ключи у словаря с постами'
        with pytest.raises(FilePostsNotExists) as exception_err:
            break_post_file.get_all_posts()
        exception_message = exception_err.value.message
        assert exception_message == 'Фаил c постами не найден', 'не верно работает исключение'

        with pytest.raises(NotExpectedType) as exception_err:
            post_file_bad_json.get_all_posts()
        exception_message = exception_err.value.message
        assert exception_message == 'Не верный формат данных', 'не верно работает исключение по содержимому файла с ' \
                                                               'posts '

    def test_get_all_comments(self, file_dao, break_post_file, post_file_bad_json):
        comments = file_dao.get_all_comments()
        assert isinstance(comments, list), 'вернулся не список с комментариями'
        assert isinstance(comments[0], dict), 'в списке не верный тип данных комментариев'
        assert len(comments) > 0, 'вернулся пустой список с комментариями'
        assert list(comments[0].keys()) == ["post_id",
                                            "commenter_name",
                                            "comment",
                                            "pk"
                                            ], 'не совпадают ключи в комментариях'

        with pytest.raises(FileCommentsNotExists) as exception_err:
            break_post_file.get_all_comments()
        exception_message = exception_err.value.message
        assert exception_message == 'Фаил c комментариями не найден', 'не верно работает исключение'

        with pytest.raises(NotExpectedType) as exception_err:
            post_file_bad_json.get_all_comments()
        exception_message = exception_err.value.message
        assert exception_message == 'Не верный формат данных', 'не верно работает исключение по содержимому файла с ' \
                                                               'posts '


class TestPostDao:
    def test_get_number_comments_with_post_id(self, post_dao, file_dao_bad_content):
        dict_number_comments = post_dao.get_number_comments_with_post_id()
        assert type(dict_number_comments) == dict, 'не верный тип данных'

        with pytest.raises(DictKeyNotFoundError) as exception_err:
            file_dao_bad_content.get_number_comments_with_post_id()
        exception_message = exception_err.value.message
        assert exception_message == 'Ошибка обращения к данным (ключ не найден)', 'не верно работает исключение по ' \
                                                                                  'содержимому файла с comments '

    def test_get_post_for_pk(self, post_dao, file_dao_bad_content):
        post = post_dao.get_post_for_pk(1)
        assert isinstance(post, list), 'не верный формат поста'
        assert list(post[0].keys()) == ["poster_name",
                                        "poster_avatar",
                                        "pic",
                                        "content",
                                        "views_count",
                                        "likes_count",
                                        "pk"
                                        ], 'не совпадают ключи у словаря с постами'

        with pytest.raises(DictKeyNotFoundError) as exception_err:
            file_dao_bad_content.get_post_for_pk(1)
        exception_message = exception_err.value.message
        assert exception_message == 'Ошибка обращения к данным (ключ не найден)', 'не верно работает исключение по ' \
                                                                                  'содержимому файла с comments '
        with pytest.raises(PageNotFoundError) as exception_err:
            post_dao.get_post_for_pk(-1)
        exception_message = exception_err.value.message
        assert exception_message == 'Упс, нет такой страницы', 'не работает исключение на несуществующую страницу поста'

    def test_get_comments_for_post_by_pk(self, post_dao):
        comments = post_dao.get_comments_for_post_by_pk(1)
        assert isinstance(comments, list), 'вернулся не список с комментариями'
        assert isinstance(comments[0], dict), 'в списке не верный тип данных комментариев'
        assert len(comments) > 0, 'вернулся пустой список с комментариями'
        assert list(comments[0].keys()) == ["post_id",
                                            "commenter_name",
                                            "comment",
                                            "pk"
                                            ], 'не совпадают ключи в комментариях'

    def test_search_posts(self, post_dao):
        posts = post_dao.search_posts('')
        assert isinstance(posts, list), 'вернулся не список с постами'
        assert isinstance(posts[0], dict), 'в списке не верный тип данных постов'
        assert len(posts) > 0, 'вернулся пустой список с постами'
        assert list(posts[0].keys()) == ["poster_name",
                                         "poster_avatar",
                                         "pic",
                                         "content",
                                         "views_count",
                                         "likes_count",
                                         "pk"
                                         ], 'не совпадают ключи у словаря с постами'

    def test_get_bookmark_posts(self, file_dao_test_posts):
        assert isinstance(file_dao_test_posts.get_bookmark_posts([1]), list), 'ошибка обработки списка с закладками'

    def test_add_new_comment(self, file_dao_test_comments):
        data_length = len(file_dao_test_comments.get_all_comments())
        file_dao_test_comments.add_new_comment('test', 'test', 1)
        new_data_length = len(file_dao_test_comments.get_all_comments())
        assert data_length + 1 == new_data_length, 'проблемы с записью в файл с комментариями'

    def test_update_likes_post(self, file_dao_test_posts):
        post = file_dao_test_posts.get_post_for_pk(1)
        likes_count = post[0]['likes_count']
        file_dao_test_posts.update_likes_post(1, 'like')
        post = file_dao_test_posts.get_post_for_pk(1)
        new_likes_count = post[0]['likes_count']
        assert likes_count + 1 == new_likes_count, 'проблемы с функцией добавления лайков'

        post = file_dao_test_posts.get_post_for_pk(1)
        likes_count = post[0]['likes_count']
        file_dao_test_posts.update_likes_post(1, 'dislike')
        post = file_dao_test_posts.get_post_for_pk(1)
        new_likes_count = post[0]['likes_count']
        assert likes_count - 1 == new_likes_count, 'проблемы с функцией уменьшения лайков'

        result = file_dao_test_posts.update_likes_post(1)
        assert isinstance(result, int), 'вернулся не верный тип данных'

    def test_update_views_post(self, file_dao_test_posts):
        post = file_dao_test_posts.get_post_for_pk(1)
        view_count = post[0]['views_count']
        file_dao_test_posts.update_views_post(1)
        post = file_dao_test_posts.get_post_for_pk(1)
        new_view_count = post[0]['views_count']
        assert view_count + 1 == new_view_count, 'проблемы с функцией подсчета просмотров'

    def test_get_all_post_by_user_name(self, file_dao_test_posts):
        assert isinstance(file_dao_test_posts.get_all_post_by_user_name('leo'), list), 'вернулся не верный тип данных'
