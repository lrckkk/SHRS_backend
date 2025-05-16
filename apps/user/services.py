from apps.user.models import User
from core.extensions import db
from utils.commonresponse import make_response


def add_user():
    me = User(id='dsdfdsafasfas', username='admin')
    db.session.add(me)
    db.session.commit()
    print(me.id)
    print(me.username)
    print(me)
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user
    return None
