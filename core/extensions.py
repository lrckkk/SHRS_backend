# from flask_redis import FlaskRedis
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
# from flask_mail import Mail
# from flask_restx import Api
# from flask_cors import CORS
#
# # 先创建扩展对象，后在工厂中初始化
# db = SQLAlchemy()
# jwt = JWTManager()
# mail = Mail()
# api = Api(version='1.0', title='Smart Housing Rental System', description='Smart Housing Rental System', doc='/docs')
# cors = CORS()
# redis = FlaskRedis()
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# 初始化扩展实例
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def init_extensions(app):
    """初始化扩展"""
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)