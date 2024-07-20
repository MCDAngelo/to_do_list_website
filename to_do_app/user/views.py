from flask import Blueprint, render_template
from flask_login import login_required, current_user

from to_do_app.database import db
from to_do_app.public.models import ToDoList


blueprint = Blueprint("user", __name__)


@blueprint.route("/my_lists/")
@login_required
def users_lists():
    print(current_user.id)
    lists = (
        db.session.execute(
            db.select(ToDoList)
            .where(ToDoList.user_id == current_user.id)
            .order_by(ToDoList.created_at)
        )
        .scalars()
        .all()
    )
    return render_template("users_lists.html", user_lists=lists)
