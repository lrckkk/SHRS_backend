import uuid
from datetime import datetime
from core.extensions import db


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    house_id = db.Column(db.String(36), db.ForeignKey('houses.id'))
    filename = db.Column(db.String(255), nullable=False)


class House(db.Model):
    __tablename__ = 'houses'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    house_type = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(50), nullable=False)
    rent = db.Column(db.Numeric(10, 2), nullable=False)
    deposit = db.Column(db.Numeric(10, 2), nullable=False)
    decor = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='vacant', nullable=False)
    model = db.Column(db.String(50), default='no', nullable=False)
    description = db.Column(db.Text, nullable=True)
    facility = db.Column(db.Text, nullable=True)
    publish_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    images = db.relationship('Image', backref='house', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'address': self.address,
            'house_type': self.house_type,
            'area': self.area,
            'rent': float(self.rent),
            'deposit': float(self.deposit),
            'decor': self.decor,
            'status': self.status,
            'model': self.model,
            'description': self.description,
            'facility': self.facility,
            'publish_time': self.publish_time.isoformat(),
            'images': [{'id': img.id, 'url': f"/uploads/{img.filename}"} for img in self.images]
        }

    @staticmethod
    def init_db():
        # 初始化数据可以根据需要调整
        rets = [
            {
                'id': str(uuid.uuid4()),
                'title': '阳光花园2室1厅',
                'address': '北京市朝阳区阳光花园1栋101',
                'house_type': '2室1厅',
                'area': '85.5',
                'rent': 4500.0,
                'deposit': 9000.0,
                'decor': '精装修',
                'status': 'vacant',
                'model': 'yes',
                'description': '南北通透，采光良好',
                'facility': '空调,冰箱,洗衣机',
                'publish_time': datetime.now()
            },
            {
                'id': str(uuid.uuid4()),
                'title': '市中心豪华公寓',
                'address': '上海市黄浦区南京路100号',
                'house_type': '1室1厅',
                'area': '60.0',
                'rent': 6000.0,
                'deposit': 12000.0,
                'decor': '豪华装修',
                'status': 'vacant',
                'model': 'no',
                'description': '高端社区，配套齐全',
                'facility': '空调,冰箱,洗衣机,电视',
                'publish_time': datetime.now()
            }
        ]
        for ret in rets:
            house = House(**ret)
            db.session.add(house)
        db.session.commit()