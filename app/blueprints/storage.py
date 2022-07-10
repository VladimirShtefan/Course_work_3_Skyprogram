import json

from app.exceptions import FilePostsNotExists, NotExpectedType, FileCommentsNotExists


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
