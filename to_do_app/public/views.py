import datetime as dt
from uuid import uuid4
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from to_do_app.public.models import ToDoList, ToDoItem
from to_do_app.public.forms import ExistingItem, ListTitle, NewItem
from to_do_app.database import db
from to_do_app.extensions import login_manager
from to_do_app.user.forms import LoginForm, RegistrationForm
from to_do_app.user.models import User

blueprint = Blueprint("public", __name__)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@blueprint.route("/")
def homepage():
    return render_template("index.html")


@blueprint.route("/new", methods=["GET", "POST"])
def new_list():
    new_list_form = NewItem()
    if request.method == "POST":
        ts = dt.datetime.now().replace(microsecond=0)
        new_user = User(  # type: ignore[call-arg]
            id=uuid4().hex,
            created_at=ts,
        )
        new_list = ToDoList(  # type: ignore[call-arg]
            id=uuid4().hex,
            title=f"My List - {ts}",
            created_at=ts,
            user_id=new_user.id,
        )
        new_item = ToDoItem(  # type: ignore[call-arg]
            id=uuid4().hex,
            description=new_list_form.description.data,
            list=new_list,
            position=0,
            created_at=ts,
            last_updated=ts,
        )
        session["active_user_id"] = new_user.id
        new_user.lists.append(new_list)
        new_list.items.append(new_item)
        db.session.add(new_list)
        db.session.add(new_item)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("public.load_list", list_id=new_list.id))
    return render_template("new_list.html", form=new_list_form)


@blueprint.route("/<string:list_id>/", methods=["GET", "POST"])
def load_list(list_id):
    session["active_list_id"] = list_id
    to_do_list = db.get_or_404(ToDoList, list_id)
    list_title_form = ListTitle(list_title=to_do_list.title)
    items = (
        db.session.execute(
            db.select(ToDoItem)
            .where(ToDoItem.list_id == list_id)
            .order_by(ToDoItem.position)
        )
        .scalars()
        .all()
    )
    new_list_form = NewItem()
    new_list_form.prefix = "new_item"
    item_forms = []
    for item in items:
        item_form = ExistingItem(obj=item)
        item_form.prefix = item.id
        item_form.starred.value = True if item.starred else False
        item_forms.append(item_form)

    return render_template(
        "active_list.html",
        title_form=list_title_form,
        new_item_form=new_list_form,
        existing_items=item_forms,
    )


@blueprint.route("/add_new_item/", methods=["POST"])
def add_new_item():
    list_id = session.get("active_list_id", None)
    # Add in logic to handle list_id is None
    if list_id is not None:
        print(f"list id in public.add_new_item: {list_id}")
        if request.method == "POST":
            form = NewItem()
            if form.validate():
                ts = dt.datetime.now()
                item_list = db.get_or_404(ToDoList, list_id)
                n_items = len(item_list.items)
                new_item = ToDoItem(  # type: ignore[call-arg]
                    id=uuid4().hex,
                    description=form.description.data,
                    completed=form.completed.data,
                    list=item_list,
                    position=n_items,
                    created_at=ts,
                    last_updated=ts,
                )
                db.session.add(new_item)
                item_list.items.append(new_item)
                db.session.commit()
            return redirect(url_for("public.load_list", list_id=list_id))


@blueprint.route("/update_item/<string:item_id>/", methods=["POST"])
def update_item(item_id):
    item = db.get_or_404(ToDoItem, item_id)
    item.description = request.form.get("description")
    item.last_updated = dt.datetime.now()
    db.session.commit()
    return redirect(url_for("public.load_list", list_id=item.list_id))


@blueprint.route("/delete_item/<string:item_id>/", methods=["POST"])
def delete_item(item_id):
    item = db.get_or_404(ToDoItem, item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("public.load_list", list_id=item.list_id))


@blueprint.route("/star_item/<string:item_id>/", methods=["POST"])
def star_item(item_id):
    item = db.get_or_404(ToDoItem, item_id)
    item.starred = False if item.starred else True
    item.last_updated = dt.datetime.now()
    db.session.commit()
    return redirect(url_for("public.load_list", list_id=item.list_id))


@blueprint.route("/update_list_title/", methods=["POST"])
def update_list_title():
    list_id = session.get("active_list_id", None)
    if list_id is not None:
        to_do_list = db.get_or_404(ToDoList, list_id)
        to_do_list.title = request.form.get("list_title")
        db.session.commit()
        return redirect(url_for("public.load_list", list_id=list_id))


@blueprint.route("/move_item/<string:item_id>/<string:direction>", methods=["POST"])
def move_item(item_id, direction):
    if direction == "up":
        adj = -1
    elif direction == "down":
        adj = 1
    ts = dt.datetime.now()
    selected_item = db.get_or_404(ToDoItem, item_id)
    original_position = selected_item.position
    new_position = original_position + adj
    swapped_item = db.session.execute(
        db.select(ToDoItem).where(
            (ToDoItem.list_id == selected_item.list_id)
            & (ToDoItem.position == new_position)
        )
    ).scalar()
    selected_item.position = new_position
    selected_item.last_updated = ts
    swapped_item.position = original_position
    swapped_item.last_updated = ts
    db.session.commit()
    return redirect(url_for("public.load_list", list_id=selected_item.list_id))


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        pswd = login_form.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not user:
            flash("No account found with this email, try again or register")
            return redirect(url_for("public.login"))
        elif not check_password_hash(user.hashed_password, pswd):
            flash("Incorrect password, try again.")
            return redirect(url_for("public.login"))
        else:
            login_user(user)
            return redirect(url_for("public.homepage"))
    return render_template("login.html", form=login_form)


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        user_id = session.get("active_user_id", None)
        if reg_form.password.data != reg_form.confirm_password.data:
            flash("The passwords do not match, try again.")
            return redirect(url_for("public.register"))
        email = reg_form.email.data
        if db.session.execute(db.select(User).where(User.email == email)):
            flash(
                "You already have an account registered with this email, login instead!"
            )
            return redirect(url_for("public.login"))
        hashed_pswd = generate_password_hash(
            password=reg_form.password.data,
            method="pbkdf2:sha256",
            salt_length=8,
        )
        if user_id is None:
            user = User(  # type: ignore[call-arg]
                id=uuid4().hex,
                email=email,
                hashed_password=hashed_pswd,
                created_at=dt.datetime.now().replace(microsecond=0),
            )
            db.session.add(user)
        else:
            user = db.get_or_404(User, user_id)
            user.email = email
            user.hashed_password = hashed_pswd
        db.session.commit()
        login_user(user)
        list_id = session.get("active_list_id", None)
        if list_id is not None:
            return redirect(url_for("public.load_list", list_id=list_id))
        else:
            return redirect(url_for("public.homepage"))

    return render_template("registration.html", form=reg_form)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("public.homepage"))
