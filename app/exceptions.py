class BaseAppException(Exception):
    code = 500
    message = 'Что то пошло не так'


class FilePostsNotExists(BaseAppException):
    code = 500
    message = 'Фаил c постами не найден'


class NotExpectedType(BaseAppException):
    code = 500
    message = 'Не верный формат данных'


class FileCommentsNotExists(BaseAppException):
    code = 500
    message = 'Фаил c комментариями не найден'


class DictKeyNotFoundError(BaseAppException):
    code = 500
    message = 'Ошибка обращения к данным (ключ не найден)'


class PageNotFoundError(BaseAppException):
    code = 404
    message = 'Упс, нет такой страницы'
