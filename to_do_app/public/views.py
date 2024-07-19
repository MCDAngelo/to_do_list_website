import datetime as dt
from uuid import uuid4
from flask import Blueprint, redirect, render_template, request, url_for

from to_do_app.public.models import ToDoList, ToDoItem
from to_do_app.public.forms import ExistingItem, ListTitle, NewItem
from to_do_app.database import db

blueprint = Blueprint("public", __name__)


@blueprint.route("/")
def homepage():
    return render_template("index.html")


@blueprint.route("/new", methods=["GET", "POST"])
def new_list():
    new_list_form = NewItem()
    if request.method == "POST":
        ts = dt.datetime.now().replace(microsecond=0)
        new_list = ToDoList(  # type: ignore[call-arg]
            id=uuid4().hex,
            title=f"My List - {ts}",
            created_at=ts,
        )
        new_item = ToDoItem(  # type: ignore[call-arg]
            id=uuid4().hex,
            description=new_list_form.description.data,
            list=new_list,
            position=0,
            starred=new_list_form.new_starred.data,
            created_at=ts,
            last_updated=ts,
        )
        new_list.items.append(new_item)
        db.session.add(new_list)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("public.load_list", list_id=new_list.id))
    return render_template("new_list.html", form=new_list_form)


@blueprint.route("/<string:list_id>/", methods=["GET", "POST"])
def load_list(list_id):
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
        list_id=list_id,
    )


@blueprint.route("/add_new_item/<string:list_id>/", methods=["POST"])
def add_new_item(list_id):
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


@blueprint.route("/update_item/<string:list_id>/<string:item_id>/", methods=["POST"])
def update_item(list_id, item_id):
    item = db.get_or_404(ToDoItem, item_id)
    item.description = request.form.get("description")
    item.last_updated = dt.datetime.now()
    db.session.commit()
    return redirect(url_for("public.load_list", list_id=list_id))


@blueprint.route("/delete_item/<string:list_id>/<string:item_id>/", methods=["POST"])
def delete_item(list_id, item_id):
    item = db.get_or_404(ToDoItem, item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("public.load_list", list_id=list_id))


@blueprint.route("/star_item/<string:list_id>/<string:item_id>/", methods=["POST"])
def star_item(list_id, item_id):
    item = db.get_or_404(ToDoItem, item_id)
    item.starred = False if item.starred else True
    item.last_updated = dt.datetime.now()
    db.session.commit()
    return redirect(url_for("public.load_list", list_id=list_id))


@blueprint.route("/update_list_title/<string:list_id>", methods=["POST"])
def update_list_title(list_id):
    to_do_list = db.get_or_404(ToDoList, list_id)
    print(request.form)
    to_do_list.title = request.form.get("list_title")
    db.session.commit()
    return redirect(url_for("public.load_list", list_id=list_id))


@blueprint.route(
    "/move_item/<string:list_id>/<string:item_id>/<string:direction>", methods=["POST"]
)
def move_item(list_id, item_id, direction):
    print(f"moving item {item_id} {direction} one spot")
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
            (ToDoItem.list_id == list_id) & (ToDoItem.position == new_position)
        )
    ).scalar()
    selected_item.position = new_position
    selected_item.last_updated = ts
    swapped_item.position = original_position
    swapped_item.last_updated = ts
    db.session.commit()
    return redirect(url_for("public.load_list", list_id=list_id))


@blueprint.route("/login")
def login():
    return render_template("index.html")


@blueprint.route("/register")
def register():
    return render_template("index.html")
