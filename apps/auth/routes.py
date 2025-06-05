from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage

from .services import AuthService
from .schemas import LoginSchema, RegisterSchema
from core.exceptions import handle_api_exception, ValidationError
from flask import request, current_app
from werkzeug.utils import secure_filename
import os

# 创建认证命名空间
auth_ns = Namespace('auth', description='用户认证相关操作')
# 定义命名空间
user_ns = Namespace('user', description='用户相关操作')

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
# 图片区域
avatar_upload_model = auth_ns.model('AvatarUpload', {
    'message': fields.String(required=True, description='状态信息'),
    'avatar_url': fields.String(required=True, description='头像图片的访问URL')
})
avatar_upload_parser = reqparse.RequestParser()
avatar_upload_parser.add_argument('id', type=str, required=True, location='form', help='用户ID')
avatar_upload_parser.add_argument('image', type=FileStorage, required=True, location='files')

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





# 配置上传文件夹
UPLOAD_FOLDER = 'uploads/pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 模拟存储用户头像路径（实际项目中应存入数据库）
user_avatars = {}  # 格式：{user_id: avatar_path}

@auth_ns.route('/avatar')
class AvatarUpload(Resource):
    @auth_ns.expect(avatar_upload_parser)
    def post(self):
        """上传用户头像"""
        # 获取用户ID（这里假设前端传递了user_id，实际可以从token获取）
        user_id = request.form.get('id')
        args = avatar_upload_parser.parse_args()
        user_id = args['id']
        file = args['image']
        # if not user_id:
        #     return {'message': '缺少用户ID'}, 400

        # 检查文件
        if 'image' not in request.files:
            return {'message': '未检测到文件'}, 400
        # file = request.files['image']
        if file.filename == '':
            return {'message': '未选择文件'}, 400
        if not allowed_file(file.filename):
            return {'message': '不支持的文件类型'}, 400

        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        filename = f"{user_id}_avatar.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # 避免文件冲突，先删除已有文件
        if os.path.exists(filepath):
            os.remove(filepath)

        # 保存文件
        file.save(filepath)

        # 记录用户头像路径（实际项目应存入数据库）
        user_avatars[user_id] = filepath

        # 返回头像访问路径
        avatar_url = f'/image?path={filepath}'
        return {
            'message': '头像上传成功',
            'avatar_url': avatar_url
        }, 201
#
# # 提供图片访问接口（你之前已有的）
# @user_ns.route('/image')
# class ImageResource(Resource):
#     def get(self):
#         path = request.args.get('path')
#         if not path:
#             return {'message': '缺少路径参数'}, 400
#
#         abs_path = os.path.abspath(path)
#         upload_dir = os.path.abspath(UPLOAD_FOLDER)
#
#         # 安全检查
#         if not abs_path.startswith(upload_dir):
#             return {'message': '非法路径'}, 403
#         if not os.path.exists(abs_path):
#             return {'message': '文件不存在'}, 404
#
#         return send_file(abs_path)

