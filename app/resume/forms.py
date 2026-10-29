from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp

class ContactForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(message="Ім'я обов'язкове"),
            Length(
                min=4,
                max=10,
                message="Ім'я повинно мати від 4 до 10 символів",
            ),
        ],
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email обов’язковий'),
            Email(message='Невірний формат email'),
        ],
    )

    phone = StringField(
        'Phone',
        validators=[
            DataRequired(message='Номер телефону обов’язковий'),
            Regexp(
                r'^\+380\d{9}$',
                message='Телефон повинен бути у форматі +380XXXXXXXXX',
            ),
        ],
    )

    subject = SelectField(
        'Subject',
        choices=[
            ('support', 'Технічна підтримка'),
            ('cooperation', 'Співпраця'),
            ('question', 'Загальне питання'),
        ],
        validators=[DataRequired()],
    )

    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message="Повідомлення обов'язкове"),
            Length(max=500, message='Повідомлення не повинно перевищувати 500 символів'),
        ],
    )

    submit = SubmitField('Send Message')