# config/development.py
import os


class DevelopmentConfig:
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'dev-secret-key'  # 请在实际项目中使用更安全的密钥
    SQLALCHEMY_DATABASE_URI = 'mysql://root:xy20041004@localhost:3306/shrs'
    SQLALCHEMY_ECHO = True # 显示SQL语句
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False  # 避免中文乱码（如果有中文响应）

    JWT_SECRET_KEY = 'your-secret-key'

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = '2959209045@qq.com'
    MAIL_PASSWORD = 'fxofgplgcwnodhcf' # QQ邮箱的授权码
    MAIL_DEFAULT_SENDER = '2959209045@qq.com'

    REDIS_URL = "redis://:@localhost:6379/0"

    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    JWT_EXPIRE_MINUTES = 60 * 2  # JWT过期时间 (2小时)

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+pymysql://user:password@localhost/house_rental'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 日志配置
    LOG_LEVEL = 'DEBUG'

    # API配置
    API_TITLE = '房屋租赁系统 API'
    API_VERSION = '1.0'
    OPENAPI_VERSION = '3.0.3'

