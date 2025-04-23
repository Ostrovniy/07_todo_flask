# блюпринт для работы с задачами

# Главная страница 
# Страница редактирования определенной задачи

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# auth это имя блю принта
tasks_bp = Blueprint('tasks', __name__)


# http://127.0.0.1:5000/
@tasks_bp.route('/', methods=('GET', 'POST'))
def index():
    return 'Гравная страница сайта, форма добавления задачи и отображения задач'


# http://127.0.0.1:5000/tasks/edit/5
@tasks_bp.route('/tasks/edit/<id>', methods=('GET', 'POST'))
def edit_tasks(id):
    return f'Страница для редактирования определенной задачи {id}'


