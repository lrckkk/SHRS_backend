# from core.extensions import db
#
# class User (db.Model):
#     id = db.Column(db.String(255), primary_key=True)
#     username = db.Column(db.String(255), unique=True)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#
#
import uuid

from core.extensions import db
from datetime import datetime
import enum


class UserRole(enum.Enum):
    """用户角色枚举"""
    TENANT = 'tenant'
    LANDLORD = 'landlord'
    ADMIN = 'admin'


class User(db.Model):
    """用户模型，对应数据库中的users表"""
    __tablename__ = 'users'

    # 确保id字段有默认值生成器
    id = db.Column(
        db.String(36),  # 或使用 db.String，如果使用UUID
        primary_key=True,
        default=lambda: str(uuid.uuid4()),  # 自动生成UUID
        unique=True,
        nullable=False
    )
    username = db.Column(db.String(64), unique=True, nullable=False, comment='用户名')
    email = db.Column(db.String(120), unique=True, nullable=False, comment='邮箱')
    password_hash = db.Column(db.String(256), nullable=False, comment='加密后的密码')
    role = db.Column(db.String(20), default='user', nullable=False)

    phone = db.Column(db.String(20), unique=True, nullable=True, comment='手机号')
    phone_verified = db.Column(db.Boolean, nullable=False, default=False, comment='手机验证状态')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='创建时间')

    # MFA 相关字段
    mfa_enabled = db.Column(db.Boolean, nullable=False, default=False, comment='MFA是否启用')
    mfa_secret = db.Column(db.String(32), nullable=True, comment='MFA密钥')

    # 扩展信息字段
    full_name = db.Column(db.String(100), nullable=True, comment='姓名')
    address = db.Column(db.Text, nullable=True, comment='地址')
    # avatar = db.Column(db.String(255), nullable=True, comment='头像URL')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """设置密码"""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_id(cls, user_id):
        """根据ID获取用户"""
        return cls.query.get(user_id)

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'phone': self.phone,
            'phone_verified': self.phone_verified,
            'created_at': self.created_at.isoformat(),
            'full_name': self.full_name,
            'address': self.address,
            # 'avatar': self.avatar,
            'mfa_enabled': self.mfa_enabled
        }