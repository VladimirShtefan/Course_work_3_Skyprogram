import hashlib
import json

from werkzeug.datastructures import Headers

from app.exceptions import FileCommentsNotExists, NotExpectedType


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
