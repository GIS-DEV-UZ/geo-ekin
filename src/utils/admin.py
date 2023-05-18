from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from src.utils.ext import db

class BaseModelView(ModelView):
    pass

class UserAdminView(BaseModelView):
    pass

def register_admin(admin):
    from src.models.user import User
    admin.add_view(UserAdminView(User, db.session))