from core.extensions import db
class image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.String(50), primary_key=True)  # 用户ID
    image = db.Column(db.String(255))  # 图片路径