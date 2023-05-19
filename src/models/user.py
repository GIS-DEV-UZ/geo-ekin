from src.utils.ext import db
from src.models.base import BaseModel
from flask_login import UserMixin
from src.models.polygon import  Polygon

class User(BaseModel, UserMixin):
    __tablname__ = 'user'

    user_id = db.Column(db.String(255))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(255))
    passport = db.Column(db.String(255))
    oneid_user_id = db.Column(db.String(255))
    pinfl = db.Column(db.String(255))
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(255))
    per_adr = db.Column(db.String(255))

    password = db.Column(db.String(100))

    polygons = db.relationship('Polygon', backref='user')

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.__dict__:
                continue
            self.__dict__[key] = value
        db.session.commit()
        return self