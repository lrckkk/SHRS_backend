from flask import jsonify, current_app
import traceback  # 添加traceback模块用于获取完整堆栈信息


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
    try:
        # 记录完整的异常堆栈信息
        error_trace = traceback.format_exc()
        current_app.logger.error(f"API Exception: {str(e)}\n{error_trace}")

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

    except Exception as inner_ex:
        # 确保异常处理器本身不会引发异常
        current_app.logger.critical(f"Error in exception handler: {str(inner_ex)}")
        return jsonify({
            'error': '严重错误',
            'message': '异常处理器发生错误'
        }), 500