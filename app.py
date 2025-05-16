# app.py
import os
from flask import Flask
from apps import init_app                 # 导入应用初始化函数
from core.extensions import db, jwt, mail, api, cors, redis  # 导入Flask扩展


def create_app(config_name=None):
    # 创建应用实例
    flask_app = Flask(__name__)

    # 配置加载策略
    if not config_name:
        env = os.getenv('FLASK_ENV', 'development')
        config_name = 'production' if env == 'production' else 'development'

    # 动态加载配置类
    flask_app.config.from_object(f'config.{config_name.capitalize()}Config')

    # 初始化扩展
    initialize_extensions(flask_app)

    # 注册蓝图
    init_app(flask_app)

    # 注册错误处理
    register_error_handlers(flask_app)

    return flask_app


def initialize_extensions(flask_app):
    """扩展初始化"""
    db.init_app(flask_app)
    jwt.init_app(flask_app)
    cors.init_app(flask_app, resources={r"/api/*": {"origins": "*"}})
    mail.init_app(flask_app)
    api.init_app(flask_app)     # 注册API文档
    redis.init_app(flask_app)   # Redis初始化

    # 数据库首次运行自动创建表
    # with flask_app.app_context():
    #     db.create_all()


def register_error_handlers(flask_app):
    """全局错误处理"""
    from core.exceptions import handle_404_error

    flask_app.register_error_handler(404, handle_404_error)


if __name__ == '__main__':
    app = create_app()
    app.run(host=app.config['HOST'], port=app.config['PORT'])