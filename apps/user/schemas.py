from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from apps.user.models import User

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
