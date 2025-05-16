from flask_restx import Namespace, Resource

from apps.user.schemas import UserSchema
from apps.user.services import get_user
from core.extensions import db
from utils.commonresponse import make_response

user_ns = Namespace('user', description='User related operations')
user_schema = UserSchema(session=db.session)

@user_ns.route('/<user_id>')
class UserResource(Resource):
    def get(self, user_id):
        """Get user by ID"""
        user = user_schema.dump(get_user(user_id))
        return make_response(data=user, message='success', code=0)
