# from flask_restx import Namespace, Resource, fields
#
# from apps.user.services import add_user
# from apps.user.schemas import UserSchema
# from core.extensions import db
# from utils.commonresponse import make_response
#
# hello_ns = Namespace('hello', description='test only')
# login_model = hello_ns.model('Login', {
#     'username': fields.String(required=True),
#     'password': fields.String(required=True),
# })
#
#
# user_schema = UserSchema(session=db.session)
#
# @hello_ns.route('/')
# class HelloWorld(Resource):
#     def get(self):
#         add_user()
#         return {'message': 'Hello, World!'}
#
# @hello_ns.route('/find')
# class HelloWorl(Resource):
#     @hello_ns.expect(login_model)
#     def get(self):
#         from apps.user.services import get_user
#         user = user_schema.dump(get_user('dfa'))
#         return make_response(data=user, message='success', code=0)
# @hello_ns.route('/new')
# class HelloWor(Resource):
#     def post(self):
#         from flask import request
#         if request.is_json:
#             json_data = request.get_json()
#             user = user_schema.load(json_data)
#             print(user.id)
#             print(user.username)
