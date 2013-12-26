# Our libs
from .extensions import db

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=True)
    created_on = db.Column(db.DateTime(), nullable=False)
    _is_active = db.Column(db.Boolean())
