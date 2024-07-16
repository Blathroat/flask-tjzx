from settings import app

from app import db
with app.app_context():
    db.drop_all()
    db.create_all()
