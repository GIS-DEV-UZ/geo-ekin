from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from src.utils.ext import db
from flask_login import current_user
from flask_admin import Admin, AdminIndexView



class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.oneid_user_id in ['baxtiyor_gkk', 'eldor1997']

class BaseModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.oneid_user_id in ['baxtiyor_gkk', 'eldor1997']   


class UserAdminView(BaseModelView):
    pass

def register_admin(admin):
    from src.models.user import User
    from src.models.polygon import Polygon
    admin.add_view(BaseModelView(User, db.session))
    admin.add_view(BaseModelView(Polygon, db.session))