from flask import Blueprint, request, render_template
from functions import save_picture, add_post
from json import JSONDecodeError
import logging

# создаем блюпринт loader для загрузки новых постов
loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')


# создаем вьюшку для страницы добавления поста
@loader_blueprint.route('/post')
def post_page():
    return render_template('post_form.html')


# создаем вьюшку для страницы загруженного поста
@loader_blueprint.route('/post', methods=['POST'])
def add_post_page():
    # получение картинки и подписи из формы
    picture = request.files.get('picture')
    content = request.form.get('content')

    # вывод сообщения об ошибке загрузки, если форма пустая
    if not picture or not content:
        return 'Нет картинки или текста'
    # вывод сообщения в лог и пользователю если загружена не картинка
    if picture.filename.split('.')[-1] not in ['jpeg', 'png']:
        logging.info('Загруженный файл не картинка')
        return 'Неверное расширение файла'

    # проверка картинки, вывод в лог и пользователю если файл не найден или не был отправлен
    try:
        picture_path = '/' + save_picture(picture)
    except FileNotFoundError:
        logging.error('Файл не найден')
        return 'Файл не найден'
    except JSONDecodeError:
        return 'Невалидный файл'

    # добавление и вывод нового поста
    picture_path = '/' + save_picture(picture)
    post = add_post({'pic': picture_path, 'content': content})
    return render_template('post_uploaded.html', post=post)
