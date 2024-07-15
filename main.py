from to_do_app.app import create_app
from to_do_app.database import db


app, bootstrap = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(
        debug=True,
        host="localhost",
        port=8000,
    )
