from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

starred_label = Markup('<h2><i class="fas fa-star"></i></h2>')
tags_label = Markup('<h3><i class="fas fa-tag"></i></h3>')


class NewItem(FlaskForm):
    completed = BooleanField("", render_kw={"class": "form-check-input"})
    description = StringField(
        "",
        render_kw={
            "style": "font-size:2.0rem",
            "class": "border-0",
        },
        validators=[DataRequired(), Length(min=1, max=750)],
    )
    new_starred = SubmitField(
        label=starred_label,
        default=False,
        render_kw={
            "style": "opacity:0",
            "class": "starred_check",
        },
    )


class ExistingItem(FlaskForm):
    id = StringField(validators=[DataRequired()])
    completed = BooleanField("", render_kw={"class": "form-check-input"})
    description = StringField(
        "",
        render_kw={
            "style": "font-size:2.0rem",
            "class": "border-0",
        },
        validators=[DataRequired(), Length(min=1, max=750)],
    )
    starred = SubmitField(
        label=starred_label,
        default=False,
        render_kw={
            "style": "opacity:0",
            "class": "starred_check",
        },
    )
    # Make this a ColorField
    tagged_color = BooleanField(
        label=tags_label,
        render_kw={
            "style": "opacity:0",
            "class": "tags_check",
        },
    )
    save = SubmitField("save_button")
    delete = SubmitField(
        "X",
    )
