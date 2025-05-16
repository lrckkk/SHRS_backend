# config/development.py

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

