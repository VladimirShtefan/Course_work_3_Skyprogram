class TestAllPages:
    def test_index_page(self, test_client):
        response = test_client.get('/')
        assert response.status_code == 200, 'Не верный статус код от главной страницы'

    def test_post_page(self, test_client):
        response = test_client.get('/posts/1')
        assert response.status_code == 308, 'Не верный статус код от страницы c постом'

    def test_search_page(self, test_client):
        response = test_client.get('/search/?value=')
        assert response.status_code == 200, 'Не верный статус код от страницы c поиском постов'

    def test_user_feed_page(self, test_client):
        response = test_client.get('/users/larry')
        assert response.status_code == 200, 'Не верный статус код от страницы пользователя'
