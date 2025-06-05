from flask_restx import Namespace, Resource, fields
from .services import UserService
from .schemas import UserProfileSchema, UserPasswordSchema, AdminRoleUpdateSchema
from core.security import jwt_required, role_required
from core.exceptions import handle_api_exception
from flask import request

# 创建用户命名空间
user_ns = Namespace('user', description='用户管理相关操作')

# 用户资料模型
profile_model = user_ns.model('UserProfile', {
    'full_name': fields.String(description='姓名'),
    'phone': fields.String(description='手机号'),
    'address': fields.String(description='地址'),
    'avatar': fields.String(description='头像URL')
})

# 密码修改模型
password_model = user_ns.model('PasswordChange', {
    'old_password': fields.String(required=True, description='原密码'),
    'new_password': fields.String(required=True, description='新密码')
})


@user_ns.route('/profile')
class ProfileResource(Resource):
    @jwt_required
    @user_ns.response(200, '成功')
    def get(self):
        """获取用户资料"""
        try:
            user_id = request.current_user['sub']
            user = UserService.get_user(user_id)
            return user.to_dict()
        except Exception as e:
            return handle_api_exception(e)

    @jwt_required
    @user_ns.expect(profile_model)
    @user_ns.response(200, '更新成功')
    def put(self):
        """更新用户资料"""
        try:
            user_id = request.current_user['sub']
            # 验证请求数据
            schema = UserProfileSchema()
            data = schema.load(request.json)
            # 更新资料
            user = UserService.update_profile(user_id, data)
            return user.to_dict()
        except Exception as e:
            return handle_api_exception(e)


@user_ns.route('/password')
class PasswordResource(Resource):
    @jwt_required
    @user_ns.expect(password_model)
    @user_ns.response(200, '密码修改成功')
    def put(self):
        """修改密码"""
        try:
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
            return {'message': '密码修改成功'}
        except Exception as e:
            return handle_api_exception(e)


# 管理员相关接口
@user_ns.route('/admin/users')
class AdminUserList(Resource):
    @jwt_required
    @role_required('admin')
    @user_ns.response(200, '成功')
    def get(self):
        """获取用户列表(管理员)"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            users = UserService.list_users(page, per_page)
            return users
        except Exception as e:
            return handle_api_exception(e)


@user_ns.route('/admin/users/<int:target_user_id>/role')
class AdminRoleUpdate(Resource):
    @jwt_required
    @role_required('admin')
    @user_ns.expect(user_ns.model('RoleUpdate', {
        'role': fields.String(required=True, enum=['tenant', 'landlord', 'admin'])
    }))
    @user_ns.response(200, '用户角色更新成功')
    def put(self, target_user_id):
        """更新用户角色(管理员)"""
        try:
            # 验证请求数据
            schema = AdminRoleUpdateSchema()
            data = schema.load(request.json)
            # 更新用户角色
            user = UserService.update_user_role(target_user_id, data['role'])
            return {
                'message': '用户角色更新成功',
                'user_id': user.id,
                'new_role': user.role
            }
        except Exception as e:
            return handle_api_exception(e)