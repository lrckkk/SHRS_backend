# from flask_restx import Namespace, Resource
#
# from apps.user.schemas import UserSchema
# from apps.user.services import get_user
# from core.extensions import db
# from utils.commonresponse import make_response
#
# user_ns = Namespace('user', description='User related operations')
# user_schema = UserSchema(session=db.session)
#
# @user_ns.route('/<user_id>')
# class UserResource(Resource):
#     def get(self, user_id):
#         """Get user by ID"""
#         user = user_schema.dump(get_user(user_id))
#         return make_response(data=user, message='success', code=0)
from flask import Blueprint, request, jsonify
from .services import UserService
from .schemas import UserProfileSchema, UserPasswordSchema, AdminRoleUpdateSchema
from core.security import jwt_required, role_required
from core.exceptions import handle_api_exception

user_bp = Blueprint('user', __name__)


@user_bp.errorhandler(Exception)
def handle_exception(e):
    return handle_api_exception(e)


@user_bp.route('/api/profile', methods=['GET'])
@jwt_required
def get_profile():
    """获取用户资料"""
    user_id = request.current_user['sub']
    user = UserService.get_user(user_id)
    return jsonify(user.to_dict())


@user_bp.route('/api/profile', methods=['PUT'])
@jwt_required
def update_profile():
    """更新用户资料"""
    user_id = request.current_user['sub']

    # 验证请求数据
    schema = UserProfileSchema()
    data = schema.load(request.json)

    # 更新资料
    user = UserService.update_profile(user_id, data)
    return jsonify(user.to_dict())


@user_bp.route('/api/password', methods=['PUT'])
@jwt_required
def change_password():
    """修改密码"""
    user_id = request.current_user['sub']

    # 验证请求数据
    schema = UserPasswordSchema()
    data = schema.load(request.json)

    # 更新密码
    UserService.change_password(
        user_id,
        data['old_password'],
        data['new_password']
    )

    return jsonify({'message': '密码修改成功'})


@user_bp.route('/api/mfa/setup', methods=['POST'])
@jwt_required
def setup_mfa():
    """设置MFA"""
    user_id = request.current_user['sub']
    user = UserService.get_user(user_id)

    uri, error = UserService.setup_mfa(user)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': '请使用认证器APP扫描二维码',
        'qr_code_uri': uri
    })


@user_bp.route('/api/mfa/enable', methods=['POST'])
@jwt_required
def enable_mfa():
    """启用MFA"""
    user_id = request.current_user['sub']
    user = UserService.get_user(user_id)

    # 获取验证码
    code = request.json.get('code')
    if not code:
        return jsonify({'error': '需要提供验证码'}), 400

    success, message = UserService.enable_mfa(user, code)
    if not success:
        return jsonify({'error': message}), 400

    return jsonify({'message': message})


@user_bp.route('/api/mfa/disable', methods=['POST'])
@jwt_required
def disable_mfa():
    """禁用MFA"""
    user_id = request.current_user['sub']
    user = UserService.get_user(user_id)

    # 获取密码
    password = request.json.get('password')
    if not password:
        return jsonify({'error': '需要提供密码进行验证'}), 400

    success, message = UserService.disable_mfa(user, password)
    if not success:
        return jsonify({'error': message}), 400

    return jsonify({'message': message})


@user_bp.route('/api/admin/users', methods=['GET'])
@jwt_required
@role_required('admin')
def list_users():
    """获取用户列表(管理员)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # 限制分页大小
    if per_page > 100:
        per_page = 100

    users = UserService.list_users(page, per_page)
    return jsonify(users)


@user_bp.route('/api/admin/users/<int:target_user_id>/role', methods=['PUT'])
@jwt_required
@role_required('admin')
def update_user_role(target_user_id):
    """更新用户角色(管理员)"""
    # 验证请求数据
    schema = AdminRoleUpdateSchema()
    data = schema.load(request.json)

    # 更新用户角色
    user = UserService.update_user_role(target_user_id, data['role'])
    return jsonify({
        'message': '用户角色更新成功',
        'user_id': user.id,
        'new_role': user.role.value
    })