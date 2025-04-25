from flask import Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
from . import auth
from . import forms
from . import models
from . import db

# auth это имя блю принта
tasks_bp = Blueprint('tasks', __name__)


# http://127.0.0.1:5000/
# Только для авторизованных
@tasks_bp.route('/', methods=["GET", "POST"])
@auth.login_required
def index():
    # Создание формы
    addtaskform = forms.TaskForm()

    if addtaskform.validate_on_submit():
        # Получения значений формы
        title = addtaskform.title.data
        description = addtaskform.description.data
        current_app.logger.info(f"Форма: добавить задачу, отправка формы {title}, {description}")

        # Добавления новой заадчи в бд
        new_task = models.Task(
            title = title,
            description= description,
            user=g.user
        )

        db.db.session.add(new_task)
        db.db.session.commit()
        return redirect(url_for('tasks.index'))
    
    return render_template('index.html', addtaskform=addtaskform, tasks=g.user.tasks)


# http://127.0.0.1:5000/tasks/edit/5
@tasks_bp.route('/tasks/edit/<id>', methods=["GET", "POST"])
@auth.login_required
def edit_tasks(id):
    return render_template('edit.html')

@tasks_bp.route('/tasks/delete/<id>', methods=["POST"])
@auth.login_required
def delete_tasks(id):
    return 'Удаления задачи'


