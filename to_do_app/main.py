from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

bootstrap = Bootstrap5(app)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/new")
def new_list():
    if request.method == "POST":
        # Create list and item entries in db
        pass
    return render_template("new_list.html")


@app.route("/<str:list_id>")
def load_list():
    return render_template("new_list.html")


@app.route("/login")
def login():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(
        host="localhost",
        port=8000,
        debug=True,
    )
