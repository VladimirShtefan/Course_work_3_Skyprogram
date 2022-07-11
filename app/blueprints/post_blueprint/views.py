from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash

from flask_paginate import Pagination

from app.blueprints.auth import UserDetect
from app.blueprints.post_blueprint.dao.post_dao import Post
from app.exceptions import BaseAppException
from app.paths import DATA_JSON_PATH, COMMENTS_JSON_PATH, USERS_JSON_PATH
from app.logger import logger

post_blueprint = Blueprint('post_blueprint', __name__, template_folder='templates')


@post_blueprint.route('/', methods=['GET'])
def page_index():
    user = UserDetect(request.headers, request.remote_addr, USERS_JSON_PATH)
    user.add_new_user()

    posts = Post(DATA_JSON_PATH, COMMENTS_JSON_PATH)
    all_posts: list[dict] = posts.get_all_posts()

    comments: dict = posts.get_number_comments_with_post_id()

    likes_list = user.get_likes_list()
    bookmarks_list = user.get_bookmarks_list()
    return render_template('index.html', posts=all_posts, comments=comments,
                           likes_list=likes_list, bookmarks_list=bookmarks_list)


@post_blueprint.route('/posts/<int:post_id>/', methods=['GET', 'POST'])
def post_page(post_id: int):
    if request.method == 'POST':
        name: str = request.form.get('name')
        comment: str = request.form.get('comment')
        if name and comment:
            Post(DATA_JSON_PATH, COMMENTS_JSON_PATH).add_new_comment(name, comment, post_id)
            return redirect(url_for('post_blueprint.post_page', post_id=post_id))
        else:
            flash('Заполните все поля для добавления комментария', 'warning')
            return redirect(url_for('post_blueprint.post_page', post_id=post_id), code=302)
    else:
        user = UserDetect(request.headers, request.remote_addr, USERS_JSON_PATH)
        user.add_new_user()

        likes_list = user.get_likes_list()
        bookmarks_list = user.get_bookmarks_list()

        posts = Post(DATA_JSON_PATH, COMMENTS_JSON_PATH)
        post_list: list[dict] = posts.get_post_for_pk(post_id)
        posts.update_views_post(post_id)

        comments_text: list[dict] = posts.get_comments_for_post_by_pk(post_id)
        comments: dict = {
            post_id: len(comments_text)
        }
        return render_template('post.html', posts=post_list, comments_text=comments_text, comments=comments,
                               likes_list=likes_list, bookmarks_list=bookmarks_list)


# @post_blueprint.route('/posts/<int:post_id>/<string:like>/', methods=['POST'])
# def get_like(post_id: int, like: str):
#     user = UserDetect(request.headers, request.remote_addr, USERS_JSON_PATH)
#     user.add_new_user()
#     user.get_like(post_id)
#
#     posts = Post(DATA_JSON_PATH, COMMENTS_JSON_PATH)
#     posts.update_likes_post(post_id, like)
#     return redirect(request.referrer)


@post_blueprint.route('/posts/bookmarks/', methods=['GET', 'POST'])
def bookmark_page():
    user = UserDetect(request.headers, request.remote_addr, USERS_JSON_PATH)
    user.add_new_user()

    posts = Post(DATA_JSON_PATH, COMMENTS_JSON_PATH)
    bookmarks_list = user.get_bookmarks_list()
    bookmark_posts: list[dict] = posts.get_bookmark_posts(bookmarks_list)

    comments: dict = posts.get_number_comments_with_post_id()

    likes_list = user.get_likes_list()
    return render_template('bookmarks.html', posts=bookmark_posts, comments=comments,
                           likes_list=likes_list, bookmarks_list=bookmarks_list)


@post_blueprint.route('/posts/bookmark/<int:post_id>/', methods=['POST'])
def get_bookmark(post_id: int):
    user = UserDetect(request.headers, request.remote_addr, USERS_JSON_PATH)
    user.add_new_user()
    user.get_bookmark(post_id)
    return redirect(url_for('post_blueprint.bookmark_page'), code=302)


@post_blueprint.route('/search/', methods=['GET'])
def search_content_page():
    user = UserDetect(request.headers, request.remote_addr, USERS_JSON_PATH)
    user.add_new_user()

    likes_list = user.get_likes_list()
    bookmarks_list = user.get_bookmarks_list()

    per_page = 3
    search_content: str = request.args.get('value', '')
    page = int(request.args.get('page', 1))

    posts = Post(DATA_JSON_PATH, COMMENTS_JSON_PATH)
    list_with_search_posts: list[dict] = posts.search_posts(search_content)
    posts_slice = list_with_search_posts[(page - 1) * per_page:page * per_page]

    comments: dict = posts.get_number_comments_with_post_id()

    pagination = Pagination(page=page, total=len(list_with_search_posts),
                            per_page=per_page, search=False, css_framework='bootstrap4'
                            )
    return render_template('search.html', posts=posts_slice, comments=comments,
                           pagination=pagination, likes_list=likes_list, bookmarks_list=bookmarks_list)


@post_blueprint.route('/users/<string:username>/', methods=['GET'])
def user_posts_page(username: str):
    user = UserDetect(request.headers, request.remote_addr, USERS_JSON_PATH)
    user.add_new_user()

    likes_list = user.get_likes_list()
    bookmarks_list = user.get_bookmarks_list()

    posts = Post(DATA_JSON_PATH, COMMENTS_JSON_PATH)
    user_posts: list[dict] = posts.get_all_post_by_user_name(username)

    comments: dict = posts.get_number_comments_with_post_id()
    return render_template('user-feed.html', posts=user_posts, comments=comments,
                           likes_list=likes_list, bookmarks_list=bookmarks_list)


@post_blueprint.route('/api/posts', methods=['GET'])
def api_get_all_posts_page():
    logger.info(f'Запрос /api/posts/')
    posts = Post(DATA_JSON_PATH, COMMENTS_JSON_PATH)
    all_posts: list[dict] = posts.get_all_posts()
    return jsonify(all_posts)


@post_blueprint.route('/api/posts/<int:post_id>/', methods=['GET'])
def api_get_post_page(post_id: int):
    logger.info(f'Запрос /api/posts/{post_id}')
    posts = Post(DATA_JSON_PATH, COMMENTS_JSON_PATH)
    return jsonify(posts.get_post_for_pk(post_id))


@post_blueprint.route('/tag/<string:tag_name>/', methods=['GET'])
def search_hashtag(tag_name: str):
    user = UserDetect(request.headers, request.remote_addr, USERS_JSON_PATH)
    user.add_new_user()
    likes_list = user.get_likes_list()
    bookmarks_list = user.get_bookmarks_list()

    per_page = 3
    page = int(request.args.get('page', 1))

    posts = Post(DATA_JSON_PATH, COMMENTS_JSON_PATH)
    list_with_search_posts: list[dict] = posts.search_posts(f'#{tag_name}')
    posts_slice = list_with_search_posts[(page - 1) * per_page:page * per_page]

    comments: dict = posts.get_number_comments_with_post_id()

    pagination = Pagination(page=page, total=len(list_with_search_posts),
                            per_page=per_page, search=False, css_framework='bootstrap4'
                            )
    return render_template('tag.html', posts=posts_slice, comments=comments, pagination=pagination,
                           likes_list=likes_list, tag_name=tag_name, bookmarks_list=bookmarks_list)


@post_blueprint.app_errorhandler(BaseAppException)
def base_error_handler(e: BaseAppException):
    return jsonify({'error': e.message}), e.code


@post_blueprint.route('/posts/like_bookmark/', methods=['POST'])
def get_like_and_bookmark():
    data = request.get_data().decode('utf-8').split('&')
    post_id = int(data[0].replace('post_id=', ''))
    method = ['like' if 'like' in data[1] else 'bookmark' if 'bookmark' in data[1] else ''][0]
    user = UserDetect(request.headers, request.remote_addr, USERS_JSON_PATH)
    user.add_new_user()
    posts = Post(DATA_JSON_PATH, COMMENTS_JSON_PATH)
    status = ''
    likes_count = posts.update_likes_post(post_id)
    bookmarks_list = user.get_bookmarks_list()
    if method == 'bookmark':
        status = user.get_bookmark(post_id)
        bookmarks_list = user.get_bookmarks_list()
    elif method == 'like':
        status = user.get_like(post_id)
        if status == 'enable':
            likes_count = posts.update_likes_post(post_id, 'like')
        elif status == 'disable':
            likes_count = posts.update_likes_post(post_id, 'dislike')
    return jsonify({'status': status,
                    'bookmark_list': len(bookmarks_list),
                    'likes_count': likes_count,
                    })
