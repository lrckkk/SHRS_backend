from flask_restx import Namespace, Resource, fields
from .services import AuthService
from .schemas import LoginSchema, RegisterSchema
from core.exceptions import handle_api_exception, ValidationError
from flask import request, current_app

# 创建认证命名空间
auth_ns = Namespace('auth', description='用户认证相关操作')

# 登录模型
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, example='user@example.com'),
    'password': fields.String(required=True, example='your_password')
})

# 注册模型
register_model = auth_ns.model('Register', {
    'username': fields.String(required=True, description='用户名'),
    'email': fields.String(required=True, description='邮箱'),
    'password': fields.String(required=True, description='密码'),
    'role': fields.String(required=True, description='角色', enum=['tenant', 'landlord', 'admin'])
})


@auth_ns.route('/register')
class RegisterResource(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, '注册成功')
    @auth_ns.response(400, '验证失败')
    def post(self):
        """用户注册"""
        try:
            # 使用注册Schema验证数据
            schema = RegisterSchema()
            data = schema.load(request.json)

            # 注册用户
            user = AuthService.register_user(data)

            return {
                'message': '注册成功',
                'user_id': user.id,
                'username': user.username
            }, 201

        except Exception as e:
            return handle_api_exception(e)


@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """用户登录（使用邮箱）"""
        try:
            # 获取请求数据
            data = request.json

            # 验证输入
            if not data.get('email') or not data.get('password'):
                # 使用 ValidationError 替代自定义异常
                raise ValidationError({'message': '邮箱和密码是必填项'})

            # 认证用户
            user = AuthService.authenticate_user(
                email=data['email'],
                password=data['password']
            )

            # 生成令牌
            token = AuthService.generate_jwt_token(user)

            return {
                'access_token': token,
                'user_id': user.id,
                'role': user.role,
                'message': '登录成功'
            }, 200

        except Exception as e:
            # 使用 current_app.logger 替代 app_logger
            current_app.logger.error(f"登录失败: {str(e)}", exc_info=True)
            return handle_api_exception(e)
