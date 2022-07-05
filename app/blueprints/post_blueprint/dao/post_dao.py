from werkzeug.datastructures import Headers
import hashlib

import json

from app.exceptions import FilePostsNotExists, NotExpectedType, FileCommentsNotExists, DictKeyNotFoundError, \
    PageNotFoundError


class File:
    def __init__(self, posts_file: str, comments_file: str):
        self.path_file: str = posts_file
        self.comments_file: str = comments_file

    def get_all_posts(self) -> list[dict]:
        try:
            with open(self.path_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            raise FilePostsNotExists()
        if not isinstance(data, list):
            raise NotExpectedType()
        return data

    def get_all_comments(self) -> list[dict]:
        with open(self.comments_file, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except FileNotFoundError:
                raise FileCommentsNotExists()
            if not isinstance(data, list):
                raise NotExpectedType()
        return data

    def write_comments(self, data: list[dict]) -> None:
        with open(self.comments_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def update_posts(self, data: list[dict]):
        with open(self.path_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


class Post(File):
    def get_number_comments_with_post_id(self) -> dict:
        comments: list[dict] = self.get_all_comments()
        comments_dict = {}
        for comment in comments:
            try:
                if comment['post_id'] in comments_dict.keys():
                    comments_dict[comment['post_id']] += 1
                else:
                    comments_dict[comment['post_id']] = 1
            except KeyError:
                raise DictKeyNotFoundError()
        return comments_dict

    def get_post_for_pk(self, pk: int) -> dict:
        posts = self.get_all_posts()
        for post in posts:
            try:
                if post['pk'] == pk:
                    words: list = post['content'].split(' ')
                    for index, word in enumerate(words):
                        if word.startswith('#'):
                            hashtag = word.replace('#', '')
                            word = f'<a href="/tag/{hashtag}">{word}</a>'
                            words[index] = word
                    post['content'] = ' '.join(words)
                    return post
            except KeyError:
                raise DictKeyNotFoundError()
        raise PageNotFoundError()

    def get_bookmark_posts(self, bookmark_list: list) -> list[dict]:
        posts = self.get_all_posts()
        bookmark_posts = []
        for post in posts:
            if post['pk'] in bookmark_list:
                bookmark_posts.append(post)
        return bookmark_posts

    def get_comments_for_post_by_pk(self, pk: int) -> list[dict]:
        comments = self.get_all_comments()
        comments_list = [comment for comment in comments if comment['post_id'] == pk]
        return comments_list

    def search_posts(self, search_content: str) -> list[dict]:
        posts = self.get_all_posts()
        search_posts_list = [post for post in posts if search_content.lower() in post['content'].lower()]
        return search_posts_list

    def add_new_comment(self, name: str, comment: str, post_id: int):
        all_comments = self.get_all_comments()
        all_comments.append({
                            "post_id": post_id,
                            "commenter_name": name,
                            "comment": comment,
                            "pk": len(all_comments) + 1
                            })
        self.write_comments(all_comments)

    def update_likes_post(self, post_id, like: str):
        posts = self.get_all_posts()
        for post in posts:
            if post["pk"] == post_id and like == 'like':
                post['likes_count'] += 1
            elif post["pk"] == post_id and like == 'dislike':
                post['likes_count'] -= 1
        self.update_posts(posts)

    def update_views_post(self, post_id: int):
        posts = self.get_all_posts()
        for post in posts:
            if post["pk"] == post_id:
                post['views_count'] += 1
        self.update_posts(posts)


class User(Post):
    def get_all_post_by_user_name(self, user_name: str) -> list[dict]:
        posts = self.get_all_posts()
        user_posts = [post for post in posts if user_name in post['poster_name']]
        return user_posts


class UserDetect:
    def __init__(self, user_info: Headers, remote_addr: str, path: str):
        self.user_info = user_info
        self.remote_addr = remote_addr
        self.path = path

    def get_md5_for_user(self):
        hash_object = hashlib.md5(''.join([self.remote_addr,
                                           self.user_info['User-Agent'],
                                           self.user_info['Accept-Language']]
                                          ).encode())
        return hash_object.hexdigest()

    def load_users(self) -> list[dict]:
        with open(self.path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except FileNotFoundError:
                raise FileCommentsNotExists()
            if not isinstance(data, list):
                raise NotExpectedType()
        return data

    def write_user(self, data: list[dict]):
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_all_users_md5(self):
        all_users = self.load_users()
        return [user['user_md5'] for user in all_users]

    def add_new_user(self):
        users_md5 = self.get_all_users_md5()
        user_md5 = self.get_md5_for_user()
        users: list[dict] = self.load_users()
        if user_md5 not in users_md5:
            user_data = {
                "user_md5": user_md5,
                "pk_posts_with_like": [],
                "pk_posts_in_bookmarks": [],
                "pk": len(users) + 1
            }
            users.append(user_data)
            self.write_user(users)

    def get_like(self, post_id: int = None, like: str = None):
        user_md5 = self.get_md5_for_user()
        users: list[dict] = self.load_users()
        for user in users:
            if user['user_md5'] == user_md5:
                if like == 'like':
                    temp_list = user['pk_posts_with_like']
                    temp_list.append(post_id)
                    user['pk_posts_with_like'] = list(set(temp_list))
                elif like == 'dislike':
                    temp_list = user['pk_posts_with_like']
                    temp_list.remove(post_id)
                    user['pk_posts_with_like'] = list(set(temp_list))
                self.write_user(users)

    def get_bookmark(self, post_id: int = None, bookmark: str = None):
        user_md5 = self.get_md5_for_user()
        users: list[dict] = self.load_users()
        for user in users:
            if user['user_md5'] == user_md5:
                if bookmark == 'add':
                    temp_list = user['pk_posts_in_bookmarks']
                    temp_list.append(post_id)
                    user['pk_posts_in_bookmarks'] = list(set(temp_list))
                elif bookmark == 'remove':
                    temp_list = user['pk_posts_in_bookmarks']
                    temp_list.remove(post_id)
                    user['pk_posts_in_bookmarks'] = list(set(temp_list))
                self.write_user(users)

    def get_likes_list(self):
        users_md5 = self.get_all_users_md5()
        user_md5 = self.get_md5_for_user()
        users: list[dict] = self.load_users()
        if user_md5 in users_md5:
            for user in users:
                if user['user_md5'] == user_md5:
                    return user["pk_posts_with_like"]

    def get_bookmarks_list(self):
        users_md5 = self.get_all_users_md5()
        user_md5 = self.get_md5_for_user()
        users: list[dict] = self.load_users()
        if user_md5 in users_md5:
            for user in users:
                if user['user_md5'] == user_md5:
                    return user["pk_posts_in_bookmarks"]
