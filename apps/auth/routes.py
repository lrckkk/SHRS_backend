from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource

from apps.auth.services import auth_user
from apps.user.models import User
from apps.user.schemas import UserSchema
from core.extensions import db, redis
from utils.cache import verify_code_cache
from utils.commonresponse import make_response, handle_code
from utils.email import send_verification_code
from utils.generateid import generate_id

auth_ns = Namespace('Auth', description='User related operations')
auth_schema = UserSchema(session=db.session)

#提供账号密码，验证用户
@auth_ns.route('/users')
class AuthUsers(Resource):
    @auth_ns.doc(params={'email': 'email', 'password': 'password'})
    def get(self):
        email = request.args.get('email')
        password = request.args.get('password')
        code = auth_user(email, password)
        if code == 200:
            #发送验证码
            verification_code = send_verification_code(email)
            verify_code_cache[email] = verification_code#存验证码
            return make_response(message='verification code has been sent', code=code)
        return handle_code(code)
        #生成token
        #
        # return make_response(data=token, message='success', code=0)
    def post(self):
        email = request.form['email']
        password = request.form['password']
        code = request.form.get('code')

        if not code:
            sent_code = send_verification_code(email)
            verify_code_cache[email] = sent_code
            return make_response(message='verification code has been sent', code=200)
        if code != verify_code_cache.get(email):
            return make_response(message='verification code is wrong', code=400)
        del verify_code_cache[email]# 删除验证码
        user_id = generate_id()
        new_user = User(id=user_id, username=user_id ,email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return make_response(message='user created successfully', code=200)

#提供邮箱验证码，二重验证
@auth_ns.route('/emails')
class AuthEmails(Resource):
    @auth_ns.doc(params={'email': 'email', 'code': 'verification code'})
    def get(self):
        email = request.args.get('email')
        verification_code = request.args.get('code')
        real_code = verify_code_cache.get(email)
        if real_code is None:
            return make_response(message='verification code has expired', code=300)
        if verification_code != real_code:
            return make_response(message='verification code is wrong', code=400)
        del verify_code_cache[email]  # 删除验证码
        token = create_access_token(identity=email)
        return make_response(data=token, message='success', code=200)

    @auth_ns.route('/redis')
    class AuthRedis(Resource):
        def get(self):
            print(redis.get('name'))
            return make_response(data=redis.get('name').decode('utf-8'), message='success', code=200)