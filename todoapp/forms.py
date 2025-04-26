from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class TaskForm(FlaskForm):
    status = BooleanField(label='Статус')
    title = StringField('Название', validators=[DataRequired(), Length(min=1, max=100)])
    description = StringField('Описание', validators=[Length(min=0, max=250)])
    submit = SubmitField('Сохранить')