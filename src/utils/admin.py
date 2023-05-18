from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from src.utils.ext import db

class BaseModelView(ModelView):
    pass

class UserAdminView(BaseModelView):
    pass

def register_admin(admin):
    from src.models.user import User
    from src.models.polygon import Polygon
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Polygon, db.session))