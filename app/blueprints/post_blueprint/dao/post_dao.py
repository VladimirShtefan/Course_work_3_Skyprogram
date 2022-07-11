from app.exceptions import DictKeyNotFoundError, PageNotFoundError
from app.blueprints.storage import File


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

    def get_post_for_pk(self, pk: int) -> list[dict]:
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
                    return [post]
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

    def update_likes_post(self, post_id, like: str = None):
        posts = self.get_all_posts()
        for post in posts:
            if post["pk"] == post_id and like == 'like':
                post['likes_count'] += 1
                self.update_posts(posts)
                return post['likes_count']
            elif post["pk"] == post_id and like == 'dislike':
                post['likes_count'] -= 1
                self.update_posts(posts)
                return post['likes_count']
            elif post["pk"] == post_id and like is None:
                return post['likes_count']

    def update_views_post(self, post_id: int):
        posts = self.get_all_posts()
        for post in posts:
            if post["pk"] == post_id:
                post['views_count'] += 1
        self.update_posts(posts)

    def get_all_post_by_user_name(self, user_name: str) -> list[dict]:
        posts = self.get_all_posts()
        user_posts = [post for post in posts if user_name in post['poster_name']]
        return user_posts
