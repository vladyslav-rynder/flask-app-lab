from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField(
        'Title', validators=[DataRequired(), Length(min=2, max=150)]
    )
    content = TextAreaField('Content', validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)
    author = StringField('Author', validators=[Length(max=20)], default='Anonymous')
    category = SelectField(
        'Category',
        choices=[
            ('news', 'News'),
            ('publication', 'Publication'),
            ('tech', 'Tech'),
            ('other', 'Other'),
        ],
        default='news',
    )
    submit = SubmitField('Save Post')