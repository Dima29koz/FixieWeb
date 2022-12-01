from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email


class IncidentForm(FlaskForm):
    name = StringField("ФИО:", validators=[DataRequired('Поле не заполнено')])
    email = EmailField('Почта:', validators=[DataRequired(),
                                             Email(message='Введен некорректный email адрес')])

    subject = StringField('Тема', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField("Отправить")
