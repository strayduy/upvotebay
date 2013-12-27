# Standard libs
from datetime import datetime

# Third party libs
from flask.ext.login import UserMixin

# Our libs
from .extensions import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    email = db.Column(db.String(256), nullable=True)
    created_on = db.Column(db.DateTime(), nullable=False)
    _is_active = db.Column(db.Boolean(), default=True)
    oauth_scope = db.Column(db.Text(), nullable=True)
    oauth_access_token = db.Column(db.Text(), nullable=True)
    oauth_refresh_token = db.Column(db.Text(), nullable=True)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(int(user_id))

    def __init__(self, username=None,
                       email=None,
                       created_on=None,
                       _is_active=True,
                       oauth_scope=None,
                       oauth_access_token=None,
                       oauth_refresh_token=None):
        self.username = username
        self.email = email
        if created_on:
            self.created_on = created_on
        else:
            self.created_on = datetime.utcnow()
        self._is_active = _is_active
        self.oauth_scope = oauth_scope
        self.oauth_access_token = oauth_access_token
        self.oauth_refresh_token = oauth_refresh_token

    def is_active(self):
        return self._is_active

    def set_access_info(self, access_info):
        self.oauth_scope = ','.join(list(access_info['scope']))
        self.oauth_access_token = access_info['access_token']
        self.oauth_refresh_token = access_info['refresh_token']

    def __repr__(self):
        return '<User "{username}">'.format(username=self.username)
