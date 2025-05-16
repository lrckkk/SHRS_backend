def make_response(data=None, message='success', code=0):
    response = {
        'code': code,
        'message': message,
    }
    if data is not None:
        response['data'] = data
    return response

def handle_code(code):
    messages = {
        999: "User not found",
        888: "Password error",
        200: "success"
    }
    message = messages.get(code, 'Unknown error')
    return make_response(code=code, message=message,data=None)