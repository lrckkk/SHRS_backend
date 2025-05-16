# This file marks the apps directory as a package
# You can use it to organize different parts of your application
from .auth.routes import auth_ns
from .helloworld.routes import hello_ns
from core.extensions import api
from .user.routes import user_ns


def init_app(app):
    """
    Initialize and register all blueprints with the Flask application

    Args:
        app: Flask application instance
    """
    # Import and register blueprints here as your project grows
    # Example:
    # from apps.some_module.views import some_blueprint
    # app.register_blueprint(some_blueprint)
    api.add_namespace(hello_ns, path='/hello')
    api.add_namespace(user_ns, path='/user')
    api.add_namespace(auth_ns, path='/auth')


    pass