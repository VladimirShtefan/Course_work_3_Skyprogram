class TestAllPages:
    def test_post_page(self, test_client):
        response = test_client.get('/posts/1')
        assert response.status_code == 308, 'Не верный статус код от страницы c постом'

    def test_user_feed_page(self, test_client):
        response = test_client.get('/users/larry')
        assert response.status_code == 308, 'Не верный статус код от страницы пользователя'

    def test_api_get_all_posts(self, test_client):
        data = test_client.get('/api/posts')
        assert data.content_type == 'application/json', 'не верный формат данных постов в api'

    def test_api_get_post(self, test_client):
        data = test_client.get('/api/posts/1')
        assert data.content_type == 'text/html; charset=utf-8', 'не верный формат данных постов в api'
