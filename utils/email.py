import random

from flask_mail import Message

from core.extensions import mail


def send_verification_code(to_email):
    code = str(random.randint(100000, 999999))  # 6位验证码
    msg = Message(subject='验证码',
                  recipients=[to_email],
                  body=f'您的验证码是：{code}，5分钟内有效。')

    mail.send(msg)
    return code  # 可用于存入数据库或 Redis 用于校验
