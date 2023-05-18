from flask import Flask, url_for
from src.utils.ext import register_blueprints, register_extensions
from src.utils.ext import oneid


def create_app(config:str):

    app = Flask(__name__)

    if config in ['dev', 'prod', 'test']:
        app.config.from_object(f"src.utils.config.{config.capitalize()}Config")


    register_blueprints(app)
    register_extensions(app)

    with app.app_context():
        from src.utils.ext import db
        # db.drop_all()
        db.create_all()


    with app.test_request_context():
        oneid.Set_Callback(url_for('user_route.get_params'))

    return app