from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired, Length


class NewItem(FlaskForm):
    completed = BooleanField("", render_kw={"class": "form-check-input"})
    description = StringField(
        "",
        validators=[DataRequired(), Length(min=1, max=750)],
    )
    starred = BooleanField("", render_kw={"style": "opacity:0"})
    tagged_color = BooleanField(
        "",
        render_kw={"style": "opacity:0"},
    )
    deleted = BooleanField(
        "",
        render_kw={"style": "opacity:0"},
    )


class ExistingItem(FlaskForm):
    id = StringField(validators=[DataRequired()])
    completed = BooleanField("", render_kw={"class": "form-check-input"})
    description = StringField(
        "",
        validators=[DataRequired(), Length(min=1, max=750)],
    )
    starred = BooleanField("", render_kw={"style": "opacity:0"})
    tagged_color = BooleanField(
        "",
        render_kw={"style": "opacity:0"},
    )
    deleted = BooleanField(
        "",
        render_kw={"style": "opacity:0"},
    )
