from flask import Flask, render_template, url_for
import werkzeug
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

    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('error/401.html'), 401
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('error/500.html'), 500
    
    

    return app