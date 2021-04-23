from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, PasswordField, StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class ChangeForm(FlaskForm):
    value = StringField('Введите новое значение', validators=[DataRequired()])
    submit = SubmitField('Изменить')


class ItemsForm(FlaskForm):
    name = StringField('Введите название предмета', validators=[DataRequired()])
    weight = StringField('Введите вес предмета', validators=[DataRequired()])
    about = TextAreaField("Введите краткое описание*")
    submit = SubmitField('Изменить')
