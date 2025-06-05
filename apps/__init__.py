# This file marks the apps directory as a package
# You can use it to organize different parts of your application
# from .auth.routes import auth_ns
# from .helloworld.routes import hello_ns
# from core.extensions import init_extensions
# from .user.routes import user_ns
#
#
# def init_app(app):
#     """
#     Initialize and register all blueprints with the Flask application
#
#     Args:
#         app: Flask application instance
#     """
#     # Import and register blueprints here as your project grows
#     # Example:
#     # from apps.some_module.views import some_blueprint
#     # app.register_blueprint(some_blueprint)
#     init_extensions.add_namespace(hello_ns, path='/hello')
#     init_extensions.add_namespace(user_ns, path='/user')
#     init_extensions.add_namespace(auth_ns, path='/auth')
#
#
#     pass
def init_app(app, api):
    """初始化应用模块"""
    # 注册认证命名空间
    from .auth.routes import auth_ns
    api.add_namespace(auth_ns)

    # 注册用户管理命名空间
    from .user.routes import user_ns
    api.add_namespace(user_ns)
    # 其他模块初始化...
    # from .property import routes as property_routes
    # app.register_blueprint(property_routes.property_bp, url_prefix='/api/v1/properties')