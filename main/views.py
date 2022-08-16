from json import JSONDecodeError
import logging
from flask import Blueprint, request, render_template
from functions import get_posts_by_word, load_posts

# создаем блюпринт main для вывода постов
main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')


# создаем вьюшку главной страницы
@main_blueprint.route('/')
def main_page():
    return render_template('index.html')


# создаем вьюшку страницы постов по поиску
@main_blueprint.route('/search/')
def search_page():
    # достаем ключ поиска
    search_key = request.args.get('s', '')

    # записываем в лог и выводим пользователю если файл не найден или не был отправлен
    try:
        posts = get_posts_by_word(search_key)
    except FileNotFoundError:
        logging.error('Файл не найден')
        return 'Файл не найден'
    except JSONDecodeError:
        return 'Невалидный файл'

    # вывод постов по ключу поиска
    posts = get_posts_by_word(search_key)
    return render_template('post_list.html', key=search_key, posts=posts)

