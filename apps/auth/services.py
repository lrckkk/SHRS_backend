# from sqlalchemy import select
#
# from apps.user.models import User
# from core.extensions import db
# from utils.commonresponse import make_response
#
#
# def auth_user(email, password):
#     stmt = select(User).where(User.email == email)
#     print(stmt)
#     result = db.session.execute(stmt).scalar_one_or_none()
#     print(result)
#     if result is None:                                           #用户不存在
#         return 999
#     if result.password != password:                              #密码错误
#         return 888
#     return 200
from flask import current_app
from werkzeug.security import generate_password_hash
from apps.user.models import User
from apps.user.models import Landlord
from core.extensions import db
from .schemas import RegisterSchema
from core.exceptions import AuthenticationFailed
from core.security import create_jwt_token


class AuthService:
    """认证服务类"""

    @staticmethod
    def register_user(data):
        """用户注册服务"""
        # 验证数据
        schema = RegisterSchema()
        data = schema.load(data)

        # 创建用户对象
        user = User(
            username=data['username'],
            email=data['email'],
            role=data['role']
        )
        user.password_hash = generate_password_hash(data['password'])

        # 暂时隐藏
        # # 设置可选字段
        # for field in ['phone', 'full_name', 'address']:
        #     if field in data:
        #         setattr(user, field, data[field])

        # 保存到数据库
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def register_landlord(data):
        landlord = Landlord(
            _name=str(data['username']),
            _email=str(data['email']),
            _phone_number=str(data['phone']),
        )

        landlord._password = str(generate_password_hash(data['password']))
        landlord.to_dict()
        db.session.add(landlord)
        db.session.commit()
        return landlord

    @staticmethod
    def authenticate_user(email, password):
        """用户认证服务"""
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                raise AuthenticationFailed('用户不存在')
            # 使用正确的密码验证
            if not user.verify_password(password):
                raise AuthenticationFailed('密码错误')
            return user
        except Exception as e:
            # 记录详细的异常信息
            current_app.logger.error(f"认证失败: {str(e)}")
            raise AuthenticationFailed('登录失败')

    @staticmethod
    def generate_jwt_token(user):
        """生成JWT令牌"""
        token_payload = {
            'sub': user.id,
            'username': user.username,
            'role': user.role
        }
        return create_jwt_token(token_payload)
