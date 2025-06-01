# def handle_404_error(e):
#     return "404 Not Found", 404 # 或 return "404 Not Found", 404
from flask import jsonify


class APIException(Exception):
    """API基础异常类"""

    def __init__(self, message, status_code=500, errors=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or {}


class AuthenticationFailed(APIException):
    """认证失败异常"""

    def __init__(self, message='认证失败', status_code=401):
        super().__init__(message, status_code)


class PermissionDenied(APIException):
    """权限不足异常"""

    def __init__(self, message='权限不足', status_code=403):
        super().__init__(message, status_code)


class ValidationError(APIException):
    """数据验证异常"""

    def __init__(self, message='数据验证失败', errors=None, status_code=400):
        super().__init__(message, status_code, errors)


class NotFound(APIException):
    """资源未找到异常"""

    def __init__(self, message='资源未找到', status_code=404):
        super().__init__(message, status_code)


def handle_api_exception(e):
    """全局异常处理器"""
    if isinstance(e, APIException):
        response = jsonify({
            'error': e.message,
            'errors': e.errors
        })
        response.status_code = e.status_code
        return response

    # 处理未捕获的异常
    response = jsonify({
        'error': '服务器内部错误',
        'message': str(e)
    })
    response.status_code = 500
    return response