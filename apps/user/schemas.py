# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
# from apps.user.models import User
#
# class UserSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = User
#         load_instance = True
from marshmallow import Schema, fields, validate, validates


class UserProfileSchema(Schema):
    """用户资料模式"""
    full_name = fields.Str(
        validate=validate.Length(max=100),
        error_messages={'validator_failed': '姓名不能超过100个字符'}
    )
    phone = fields.Str(
        validate=validate.Length(min=10, max=20),
        error_messages={'validator_failed': '手机号长度应为10-20个字符'}
    )
    address = fields.Str(
        validate=validate.Length(max=255),
        error_messages={'validator_failed': '地址不能超过255个字符'}
    )
    avatar = fields.Str(
        validate=validate.URL(schemes=['http', 'https']),
        error_messages={'validator_failed': '无效的头像URL'}
    )


class UserPasswordSchema(Schema):
    """用户密码更改模式"""
    old_password = fields.Str(required=True, error_messages={
        'required': '原密码是必填项'
    })
    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=8),
        error_messages={
            'required': '新密码是必填项',
            'validator_failed': '新密码长度至少为8个字符'
        }
    )

class AdminRoleUpdateSchema(Schema):
    """管理员角色更新模式"""
    role = fields.Str(
        required=True,
        validate=validate.OneOf(['tenant', 'landlord', 'admin']),
        error_messages={'required': '用户角色是必填项'}
    )