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
    task = models.Task.query.filter_by(id=id, user_id=g.user.id).first()

    # Когда задача не найдена, вернуть на главную страницу
    if not task:
        return redirect(url_for('tasks.index'))
    
    addtaskform = forms.TaskForm()
    # Редактирования задачи

    # Обновления задачи в БД
    if addtaskform.validate_on_submit():

        task.title = addtaskform.title.data
        task.description = addtaskform.description.data
        db.db.session.add(task)
        db.db.session.commit()
        flash('Данные обновлены', "success")
        return redirect(url_for('tasks.index'))

    # Отображения формы с данными для редактирования
    addtaskform.title.data = task.title
    addtaskform.description.data = task.description 
    data_add = task.data_add

    return render_template('edit.html', addtaskform=addtaskform, task_id=id, data_add=data_add)

@tasks_bp.route('/tasks/delete/<id>', methods=["POST"])
@auth.login_required
def delete_tasks(id):
    task = models.Task.query.filter_by(id=id, user_id=g.user.id).first()

    # Простое удаления, также есть безопасная штука CSRF (пока не разобрался)
    if task:
        db.db.session.delete(task)
        db.db.session.commit()
        flash('Задача удалена!', "success")
        return redirect(url_for('tasks.index'))


