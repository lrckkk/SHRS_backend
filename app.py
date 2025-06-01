# # app.py
# import os
# from flask import Flask
# from apps import init_app                 # 导入应用初始化函数
# from core.extensions import db, jwt, mail, api, cors, redis  # 导入Flask扩展
#
#
# def create_app(config_name=None):
#     # 创建应用实例
#     flask_app = Flask(__name__)
#
#     # 配置加载策略
#     if not config_name:
#         env = os.getenv('FLASK_ENV', 'development')
#         config_name = 'production' if env == 'production' else 'development'
#
#     # 动态加载配置类
#     flask_app.config.from_object(f'config.{config_name.capitalize()}Config')
#
#     # 初始化扩展
#     initialize_extensions(flask_app)
#
#     # 注册蓝图
#     init_app(flask_app)
#
#     # 注册错误处理
#     register_error_handlers(flask_app)
#
#     return flask_app
#
#
# def initialize_extensions(flask_app):
#     """扩展初始化"""
#     db.init_app(flask_app)
#     jwt.init_app(flask_app)
#     cors.init_app(flask_app, resources={r"/api/*": {"origins": "*"}})
#     mail.init_app(flask_app)
#     api.init_app(flask_app)     # 注册API文档
#     redis.init_app(flask_app)   # Redis初始化
#
#     # 数据库首次运行自动创建表
#     # with flask_app.app_context():
#     #     db.create_all()
#
#
# def register_error_handlers(flask_app):
#     """全局错误处理"""
#     from core.exceptions import handle_404_error
#
#     flask_app.register_error_handler(404, handle_404_error)
#
#
# if __name__ == '__main__':
#     app = create_app()
#     app.run(host=app.config['HOST'], port=app.config['PORT'])
from flask import Flask
from config import DevelopmentConfig
from core.extensions import db, migrate
from apps import init_app as init_app_modules
from core.exceptions import handle_api_exception


def create_app(config_class=DevelopmentConfig):
    """应用工厂函数"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config_class)

    # 初始化扩展
    from core.extensions import init_extensions
    init_extensions(app)

    # 初始化应用模块
    init_app_modules(app)

    # 注册错误处理器
    app.register_error_handler(Exception, handle_api_exception)

    # 创建应用上下文
    with app.app_context():
        # 确保数据库迁移
        migrate.init_app(app, db)

        # 在首次请求时创建数据库表（仅开发环境）
        if app.config.get('FLASK_ENV') == 'development':
            @app.before_request
            def before_request_func():
                # 确保只运行一次
                if not hasattr(app, 'database_initialized'):
                    db.create_all()
                    app.database_initialized = True

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)