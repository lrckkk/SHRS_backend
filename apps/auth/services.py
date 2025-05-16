from sqlalchemy import select

from apps.user.models import User
from core.extensions import db
from utils.commonresponse import make_response


def auth_user(email, password):
    stmt = select(User).where(User.email == email)
    print(stmt)
    result = db.session.execute(stmt).scalar_one_or_none()
    print(result)
    if result is None:                                           #用户不存在
        return 999
    if result.password != password:                              #密码错误
        return 888
    return 200
