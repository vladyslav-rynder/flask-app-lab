from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import DecimalField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField(
        'Назва товару',
        validators=[
            DataRequired(message="Назва обов'язкова"),
            Length(min=3, message='Назва повинна містити мінімум 3 символи'),
        ],
    )

    content = TextAreaField(
        'Опис товару',
        validators=[
            DataRequired(message="Опис обов'язковий"),
            Length(max=500, message='Опис занадто довгий'),
        ],
    )

    price = DecimalField(
        'Ціна (грн)',
        validators=[
            DataRequired(message="Ціна обов'язкова"),
            NumberRange(min=0.01, message='Ціна має бути більшою за 0'),
        ],
        places=2,
    )

    category = SelectField(
        'Категорія',
        choices=[
            ('electronics', 'Електроніка'),
            ('clothing', 'Одяг'),
            ('books', 'Книги'),
            ('other', 'Інше'),
        ],
        validators=[DataRequired()],
    )

    quantity = IntegerField(
        'Кількість',
        validators=[
            DataRequired(message="Кількість обов'язкова"),
            NumberRange(min=0, message="Кількість не може бути від'ємною"),
        ],
    )

    image = FileField(
        'Зображення товару',
        validators=[
            FileRequired(message="Зображення обов'язкове"),
            FileAllowed(['jpg', 'jpeg', 'png'], message='Дозволені тільки файли формату PNG, JPG, JPEG!'),
        ],
    )

    submit = SubmitField('Зберегти товар')