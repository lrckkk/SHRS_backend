from flask import Blueprint, request, jsonify
from .services import AuthService
from .schemas import LoginSchema, RegisterSchema
from core.security import jwt_required
from core.exceptions import handle_api_exception
from marshmallow import ValidationError

# 创建蓝图并添加前缀
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# 全局错误处理器
@auth_bp.errorhandler(Exception)
def handle_exception(e):
    return handle_api_exception(e)


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        # 使用注册Schema验证数据
        schema = RegisterSchema()
        data = schema.load(request.json)

        # 注册用户
        user = AuthService.register_user(data)

        return jsonify({
            'message': '注册成功',
            'user_id': user.id,
            'username': user.username
        }), 201

    except ValidationError as e:
        # 处理验证错误
        return jsonify({
            'error': '数据验证失败',
            'details': e.messages
        }), 400

    except Exception as e:
        # 处理其他异常
        return jsonify({
            'error': '注册失败',
            'message': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        # 验证请求数据
        schema = LoginSchema()
        data = schema.load(request.json)

        # 认证用户
        user = AuthService.authenticate_user(data['username'], data['password'])

        # 生成JWT令牌
        token = AuthService.generate_jwt_token(user)

        return jsonify({
            'message': '登录成功',
            'access_token': token,
            'token_type': 'bearer',
            'user_id': user.id,
            'role': user.role
        })

    except ValidationError as e:
        # 处理验证错误
        return jsonify({
            'error': '数据验证失败',
            'details': e.messages
        }), 400

    except Exception as e:
        # 处理其他异常
        return jsonify({
            'error': '登录失败',
            'message': str(e)
        }), 401


# 添加根路由用于测试
@auth_bp.route('/')
def index():
    return jsonify({
        'status': 'running',
        'routes': ['/register', '/login']
    }), 200