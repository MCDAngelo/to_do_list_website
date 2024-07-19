from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


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


class ExistingItem(FlaskForm):
    id = StringField(validators=[DataRequired()])
    position = IntegerField(validators=[DataRequired()])
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
        "starred",
        default=False,
    )
    save = SubmitField("save_button")
    move_up = SubmitField("move_up")
    move_down = SubmitField("move_down")
    delete = SubmitField("X")


class ListTitle(FlaskForm):
    list_title = StringField(
        "",
        render_kw={
            "style": "font-size:3.0rem",
            "class": "border-0",
        },
        validators=[DataRequired(), Length(min=1, max=750)],
    )
