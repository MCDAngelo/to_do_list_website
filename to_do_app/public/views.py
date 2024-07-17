from uuid import uuid4
from flask import Blueprint, redirect, render_template, request, url_for

from to_do_app.public.models import ToDoList, ToDoItem
from to_do_app.public.forms import ExistingItem, NewItem
from to_do_app.database import db

blueprint = Blueprint("public", __name__)


@blueprint.route("/")
def homepage():
    return render_template("index.html")


@blueprint.route("/new", methods=["GET", "POST"])
def new_list():
    new_list_form = NewItem()
    if request.method == "POST":
        new_list = ToDoList(  # type: ignore[call-arg]
            id=uuid4().hex,
            title="testing",
        )
        new_item = ToDoItem(  # type: ignore[call-arg]
            id=uuid4().hex,
            description=new_list_form.description.data,
            list=new_list,
            list_order=0,
            starred=new_list_form.new_starred.data,
        )
        new_list.items.append(new_item)
        db.session.add(new_list)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("public.load_list", list_id=new_list.id))
        # Create list and item entries in db
    return render_template("new_list.html", form=new_list_form)


@blueprint.route("/<string:list_id>/", methods=["GET", "POST"])
def load_list(list_id):
    print(f"load list list_id: {list_id}")
    items = (
        db.session.execute(db.select(ToDoItem).where(ToDoItem.list_id == list_id))
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
            item_list = db.get_or_404(ToDoList, list_id)
            new_item = ToDoItem(  # type: ignore[call-arg]
                id=uuid4().hex,
                description=form.description.data,
                completed=form.completed.data,
                list=item_list,
            )
            db.session.add(new_item)
            item_list.items.append(new_item)
            db.session.commit()
    return redirect(url_for("public.load_list", list_id=list_id))


@blueprint.route("/update_item/<string:list_id>/<string:item_id>/", methods=["POST"])
def update_item(list_id, item_id):
    item = db.get_or_404(ToDoItem, item_id)
    print("item description from form")
    print(request.form.get("description"))
    item.description = request.form.get("description")
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
    db.session.commit()
    return redirect(url_for("public.load_list", list_id=list_id))


@blueprint.route("/login")
def login():
    return render_template("index.html")


@blueprint.route("/register")
def register():
    return render_template("index.html")
