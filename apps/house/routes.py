from flask_restx import Namespace, Resource, fields
from flask import request
from .services import HouseService
from core.security import jwt_required
from core.exceptions import handle_api_exception

house_ns = Namespace('houses', description='房源管理相关操作')

# 响应模型
house_model = house_ns.model('House', {
    'id': fields.String(description='房源ID'),
    'title': fields.String(required=True, description='房源标题'),
    'address': fields.String(required=True, description='地址'),
    'house_type': fields.String(required=True, description='户型'),
    'area': fields.String(required=True, description='面积'),
    'rent': fields.Float(required=True, description='租金'),
    'deposit': fields.Float(required=True, description='押金'),
    'decor': fields.String(description='装修情况'),
    'status': fields.String(description='状态'),
    'model': fields.String(description='是否样板间'),
    'description': fields.String(description='描述'),
    'facility': fields.String(description='设施'),
    'publish_time': fields.DateTime(description='发布时间'),
    'images': fields.List(fields.Nested(house_ns.model('Image', {
        'id': fields.String,
        'url': fields.String
    })))
})

# 创建/更新模型
house_input_model = house_ns.model('HouseInput', {
    'title': fields.String(required=True, description='房源标题'),
    'address': fields.String(required=True, description='地址'),
    'house_type': fields.String(required=True, description='户型'),
    'area': fields.String(required=True, description='面积'),
    'rent': fields.Float(required=True, description='租金'),
    'deposit': fields.Float(required=True, description='押金'),
    'decor': fields.String(description='装修情况'),
    'status': fields.String(description='状态'),
    'model': fields.String(description='是否样板间'),
    'description': fields.String(description='描述'),
    'facility': fields.String(description='设施')
})


@house_ns.route('/')
class HouseListResource(Resource):
    @house_ns.marshal_list_with(house_model)
    def get(self):
        """获取所有房源列表"""
        try:
            return HouseService.get_all_houses()
        except Exception as e:
            return handle_api_exception(e)

    @jwt_required
    @house_ns.expect(house_input_model)
    @house_ns.marshal_with(house_model, code=201)
    def post(self):
        """创建新房源"""
        try:
            data = request.get_json()
            house = HouseService.create_house(data)
            return house, 201
        except Exception as e:
            return handle_api_exception(e)


@house_ns.route('/<string:house_id>')
class HouseResource(Resource):
    @house_ns.marshal_with(house_model)
    def get(self, house_id):
        """获取单个房源详情"""
        try:
            return HouseService.get_house_by_id(house_id)
        except Exception as e:
            return handle_api_exception(e)

    @jwt_required
    @house_ns.expect(house_input_model)
    @house_ns.marshal_with(house_model)
    def put(self, house_id):
        """更新房源信息"""
        try:
            data = request.get_json()
            return HouseService.update_house(house_id, data)
        except Exception as e:
            return handle_api_exception(e)

    @jwt_required
    @house_ns.response(204, '删除成功')
    def delete(self, house_id):
        """删除房源"""
        try:
            HouseService.delete_house(house_id)
            return '', 204
        except Exception as e:
            return handle_api_exception(e)


@house_ns.route('/<string:house_id>/images')
class HouseImagesResource(Resource):
    @house_ns.response(200, '成功', fields.List(fields.Nested(house_ns.model('Image', {
        'id': fields.String,
        'url': fields.String
    }))))
    def get(self, house_id):
        """获取房源图片列表"""
        try:
            images = HouseService.get_house_images(house_id)
            return [{'id': img.id, 'url': f"/uploads/{img.filename}"} for img in images]
        except Exception as e:
            return handle_api_exception(e)

    @jwt_required
    @house_ns.response(201, '上传成功')
    def post(self, house_id):
        """上传房源图片"""
        try:
            if 'files' not in request.files:
                return {'message': '未选择文件'}, 400

            files = request.files.getlist('files')
            uploaded_files = HouseService.upload_house_images(house_id, files)
            return {'message': '图片上传成功', 'files': uploaded_files}, 201
        except Exception as e:
            return handle_api_exception(e)


@house_ns.route('/<string:house_id>/images/<string:image_id>')
class HouseImageResource(Resource):
    @jwt_required
    @house_ns.response(204, '删除成功')
    def delete(self, house_id, image_id):
        """删除房源图片"""
        try:
            HouseService.delete_house_image(image_id)
            return '', 204
        except Exception as e:
            return handle_api_exception(e)