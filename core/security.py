import jwt
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from functools import wraps
from core.exceptions import AuthenticationFailed, PermissionDenied


def create_jwt_token(payload):
    """创建JWT令牌"""
    # 设置过期时间
    expire_delta = timedelta(minutes=current_app.config.get('JWT_EXPIRE_MINUTES', 120))
    expire_time = datetime.utcnow() + expire_delta

    # 构建有效载荷
    payload.update({
        'sub': payload.get('sub'),  # 确保包含subject字段
        'exp': expire_time,
        'iat': datetime.utcnow(),
        'iss': 'house-rental-system'
    })

    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def decode_jwt_token(token):
    """解码JWT令牌"""
    try:
        return jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256'],
            options={'verify_iss': True}
        )
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('令牌已过期')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('无效的令牌')


def jwt_required(func):
    """JWT认证装饰器"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        # 从Authorization头获取令牌
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('缺少认证信息')

        token = auth_header.split(' ')[1]

        try:
            # 解码并验证令牌
            payload = decode_jwt_token(token)
            request.current_user = payload
            return func(*args, **kwargs)
        except AuthenticationFailed as e:
            return jsonify({'error': str(e)}), 401

    return decorated_function


def role_required(role):
    """角色权限装饰器"""

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            # 首先确保有当前用户信息
            if not hasattr(request, 'current_user'):
                raise AuthenticationFailed('用户未认证')

            # 检查用户角色
            user_role = request.current_user.get('role')
            if user_role != role:
                raise PermissionDenied('权限不足')

            return func(*args, **kwargs)

        return decorated_function

    return decorator