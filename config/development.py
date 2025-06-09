import os


class DevelopmentConfig:
    # 应用基础配置
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_super_secret_key_12345!'  # 只定义一个

    # 数据库配置 (关键修复)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:liu123@localhost:3306/shrs'
    SQLALCHEMY_ECHO = True  # 显示SQL语句
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 只保留一个

    # 国际化和编码
    JSON_AS_ASCII = False  # 避免中文乱码

    # JWT配置
    JWT_SECRET_KEY = 'your-secret-key'  # 建议设置为更复杂的值

    # 邮件配置 (已正确)
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True  # TLS和SSL互斥
    MAIL_USE_SSL = False  # 明确禁用SSL
    MAIL_USERNAME = '2959209045@qq.com'
    MAIL_PASSWORD = 'fxofgplgcwnodhcf'
    MAIL_DEFAULT_SENDER = '2959209045@qq.com'

    # Redis配置
    REDIS_URL = "redis://:@localhost:6379/0"

    # JWT过期时间 (2小时)
    JWT_EXPIRE_MINUTES = 60 * 2

    # 日志配置
    LOG_LEVEL = 'DEBUG'

    # API配置
    API_TITLE = '房屋租赁系统 API'
    API_VERSION = '1.0'
    OPENAPI_VERSION = '3.0.3'

