# # apps/auth/schemas.py
# from marshmallow import Schema, fields, validate
#
# class LoginSchema(Schema):
#     username = fields.Str(required=True)
#     password = fields.Str(required=True)
#
# class RegisterSchema(Schema):
#     username = fields.Str(required=True, validate=validate.Length(min=3, max=64))
#     email = fields.Email(required=True)
#     password = fields.Str(required=True, validate=validate.Length(min=8))
#     role = fields.Str(required=True, validate=validate.OneOf(['tenant', 'landlord', 'admin']))
from marshmallow import Schema, fields, validate, validates, ValidationError
from apps.user.models import User


class LoginSchema(Schema):
    """登录请求模式"""
    username = fields.Str(required=True, error_messages={
        'required': '用户名是必填项'
    })
    password = fields.Str(required=True, error_messages={
        'required': '密码是必填项'
    })


class RegisterSchema(Schema):
    """注册请求模式"""
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=64),
        error_messages={
            'required': '用户名是必填项',
            'validator_failed': '用户名长度应为3-64个字符'
        }
    )
    email = fields.Email(required=True, error_messages={
        'invalid': '无效的邮箱格式',
        'required': '邮箱是必填项'
    })
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8),
        error_messages={
            'required': '密码是必填项',
            'validator_failed': '密码长度至少为8个字符'
        }
    )
    role = fields.Str(
        required=True,
        validate=validate.OneOf(['tenant', 'landlord', 'admin'], error='无效的用户角色'),
        error_messages={'required': '用户角色是必填项'}
    )
    phone = fields.Str(
        validate=validate.Length(min=10, max=20),
        error_messages={'validator_failed': '手机号长度应为10-20个字符'}
    )

    @validates('username')
    def validate_username(self, value):
        """验证用户名唯一性"""
        if User.query.filter_by(username=value).first():
            raise ValidationError('该用户名已被使用')

    @validates('email')
    def validate_email(self, value):
        """验证邮箱唯一性"""
        if User.query.filter_by(email=value).first():
            raise ValidationError('该邮箱已被注册')

    @validates('phone')
    def validate_phone(self, value):
        """验证手机号唯一性"""
        if value and User.query.filter_by(phone=value).first():
            raise ValidationError('该手机号已被使用')