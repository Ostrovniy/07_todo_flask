# блюпринт для работы с задачами

# Главная страница 
# Страница редактирования определенной задачи

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# auth это имя блю принта
tasks_bp = Blueprint('tasks', __name__)


# http://127.0.0.1:5000/
@tasks_bp.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


# http://127.0.0.1:5000/tasks/edit/5
@tasks_bp.route('/tasks/edit/<id>', methods=["GET", "POST"])
def edit_tasks(id):
    return render_template('edit.html')

@tasks_bp.route('/tasks/delete/<id>', methods=["POST"])
def delete_tasks(id):
    return 'Удаления задачи'


