from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_oneid import OneID
from flask_login import LoginManager

db = SQLAlchemy()
admin = Admin()
oneid = OneID()
login_manager = LoginManager()




from src.utils.admin import MyAdminIndexView, register_admin


def register_extensions(app):

    db.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())
    oneid.init_app(app)
    login_manager.init_app(app)
    register_admin(admin)


    @login_manager.user_loader
    def load_user(id):
        from src.models.user import User
        return User.query.get(id)

def register_blueprints(app):
    from src.routes import user, base, auth, polygon

    app.register_blueprint(user.user_route)
    app.register_blueprint(base.base_router)
    app.register_blueprint(auth.auth_router)
    app.register_blueprint(polygon.polygon_router)
