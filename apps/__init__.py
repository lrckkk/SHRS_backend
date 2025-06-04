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
def init_app(app):
    """初始化应用模块"""
    # 注册认证蓝图
    # 注册认证蓝图 - 移除多余的url_prefix
    from .auth.routes import auth_bp
    # 直接注册蓝图，不再添加额外的前缀
    app.register_blueprint(auth_bp)

    # 注册用户管理蓝图
    from .user.routes import user_bp
    app.register_blueprint(user_bp)

    # 其他模块初始化...
    # from .property import routes as property_routes
    # app.register_blueprint(property_routes.property_bp, url_prefix='/api/v1/properties')