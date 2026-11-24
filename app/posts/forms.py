from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length
from app import db
from app.posts.models import Tag
from app.users.models import User


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField(
        "Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()]
    )
    is_active = BooleanField("Active Post", default=True)
    publish_date = DateTimeLocalField(
        "Publish Date", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    category = SelectField(
        "Category",
        choices=[
            ("news", "News"),
            ("publication", "Publication"),
            ("tech", "Tech"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
    )
    author_id = SelectField("Author", coerce=int, validators=[DataRequired()])
    tags = SelectMultipleField("Tags", coerce=int)
    submit = SubmitField("Add Post")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        authors = db.session.scalars(db.select(User).order_by(User.id)).all()
        self.author_id.choices = [(a.id, a.username) for a in authors]

        all_tags = db.session.scalars(db.select(Tag).order_by(Tag.name)).all()
        self.tags.choices = [(t.id, t.name) for t in all_tags]