# from apps.user.models import User
# from core.extensions import db
# from utils.commonresponse import make_response
#
#
# def add_user():
#     me = User(id='dsdfdsafasfas', username='admin')
#     db.session.add(me)
#     db.session.commit()
#     print(me.id)
#     print(me.username)
#     print(me)
# def get_user(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     if user:
#         return user
#     return None
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, UserRole
from core.extensions import db
from core.exceptions import NotFound, AuthenticationFailed, PermissionDenied
import secrets
from pyotp import TOTP


class UserService:
    """用户服务类"""

    @staticmethod
    def get_user(user_id):
        """获取用户信息"""
        user = User.query.get(user_id)
        if not user:
            raise NotFound('用户不存在')
        return user

    @staticmethod
    def update_profile(user_id, data):
        """更新用户资料"""
        user = User.query.get(user_id)
        if not user:
            raise NotFound('用户不存在')

        # 更新个人信息
        for field in ['full_name', 'phone', 'address', 'avatar']:
            if field in data:
                setattr(user, field, data[field])

        db.session.commit()
        return user

    @staticmethod
    def change_password(user_id, old_password, new_password):
        """修改密码"""
        user = User.query.get(user_id)
        if not user:
            raise NotFound('用户不存在')

        if not user.verify_password(old_password):
            raise AuthenticationFailed('原密码错误')

        user._password = generate_password_hash(new_password)
        db.session.commit()

    @staticmethod
    def setup_mfa(user):
        """设置多因素认证"""
        if user.mfa_enabled:
            return None, 'MFA已启用'

        # 生成密钥
        secret = secrets.token_hex(16)
        user.mfa_secret = secret
        db.session.commit()

        # 生成TOTP URI
        totp = TOTP(secret)
        uri = totp.provisioning_uri(user._name, issuer_name="房屋租赁系统")

        return uri, None

    @staticmethod
    def enable_mfa(user, code):
        """启用MFA"""
        if user.mfa_enabled:
            return False, 'MFA已启用'

        # 验证MFA代码
        totp = TOTP(user.mfa_secret)
        if not totp.verify(code):
            return False, '验证码无效'

        user.mfa_enabled = True
        db.session.commit()
        return True, 'MFA启用成功'

    @staticmethod
    def disable_mfa(user, password):
        """禁用MFA"""
        if not user.mfa_enabled:
            return False, 'MFA未启用'

        if not user.verify_password(password):
            raise AuthenticationFailed('密码错误')

        user.mfa_enabled = False
        user.mfa_secret = None
        db.session.commit()
        return True, 'MFA已禁用'

    @staticmethod
    def list_users(page=1, per_page=20):
        """获取用户列表"""
        query = User.query.order_by(User.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'items': [user.to_dict() for user in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }

    @staticmethod
    def update_user_role(user_id, new_role):
        """更新用户角色"""
        user = User.query.get(user_id)
        if not user:
            raise NotFound('用户不存在')

        user.role = UserRole(new_role)
        db.session.commit()
        return user