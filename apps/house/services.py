import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from .models import House, Image
from core.extensions import db
from core.exceptions import NotFound


class HouseService:

    @staticmethod
    def get_all_houses():
        return House.query.all()

    @staticmethod
    def get_house_by_id(house_id):
        house = House.query.get(house_id)
        if not house:
            raise NotFound('房源不存在')
        return house

    @staticmethod
    def create_house(data):
        house = House(**data)
        db.session.add(house)
        db.session.commit()
        return house

    @staticmethod
    def update_house(house_id, data):
        house = House.query.get(house_id)
        if not house:
            raise NotFound('房源不存在')

        for key, value in data.items():
            if hasattr(house, key):
                setattr(house, key, value)

        db.session.commit()
        return house

    @staticmethod
    def delete_house(house_id):
        house = House.query.get(house_id)
        if not house:
            raise NotFound('房源不存在')

        # 删除关联图片（数据库记录和文件）
        for image in house.images:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        db.session.delete(house)
        db.session.commit()

    @staticmethod
    def upload_house_images(house_id, files):
        house = House.query.get(house_id)
        if not house:
            raise NotFound('房源不存在')

        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                image = Image(house_id=house_id, filename=filename)
                db.session.add(image)
                uploaded_files.append(filename)

        db.session.commit()
        return uploaded_files

    @staticmethod
    def delete_house_image(image_id):
        image = Image.query.get(image_id)
        if not image:
            raise NotFound('图片不存在')

        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        db.session.delete(image)
        db.session.commit()

    @staticmethod
    def get_house_images(house_id):
        house = House.query.get(house_id)
        if not house:
            raise NotFound('房源不存在')
        return house.images


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}