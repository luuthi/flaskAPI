# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.folder import FolderModel
from datetime import datetime
import json


class Folder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('folder_name',
                        type=unicode,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('user_name',
                        type=str,
                        required=True,
                        help="A folder must belong to a user"
                        )
    parser.add_argument('created_date',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        required=False
                        )
    parser.add_argument('folder_type',
                        type=bool,
                        required=True,
                        help="This field cannot be blank"
                        )

    @jwt_required()
    def get(self, _id):
        folder = FolderModel.get_by_id(_id)
        if folder:
            return {'Data': folder.json(), 'TotalRows': 1, 'Status': 1}
        return {'msg': 'Không tìm thấy thư mục', 'Status': 0}

    @jwt_required()
    def put(self, _id):
        data = Folder.parser.parse_args()
        folder = FolderModel.get_by_id(_id)
        if folder:
            if FolderModel.get_by_name(data['folder_name']) and FolderModel.get_by_user(data['user_name']):
                return {'Status': 0, 'msg': 'Đã có thư mục trùng tên'}

            folder.folder_name = data['folder_name']
            folder.folder_type = data['folder_type']

            try:
                folder.save_to_db()
            except:
                return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}
            return {'msg': 'Cập nhật thành công', 'Status': 1}
        else:
            return {'msg': 'Không tim thấy thư mục', 'Status': 0}

    @jwt_required()
    def delete(self, _id):
        folder = FolderModel.get_by_id(_id)

        if folder:
            folder.delete_from_db()

        return {'msg': 'Thư mục đã xóa', 'Status': 1}


class FolderList(Resource):

    @jwt_required()
    def post(self):
        data = Folder.parser.parse_args()
        folder = FolderModel(**data)
        try:
            folder.save_to_db()
        except:
            return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}

        return {'msg': 'Thêm mới thư mục thành công', 'Status': 1}


class FolderByUsername(Resource):

    @jwt_required()
    def get(self):
        parser_user = reqparse.RequestParser()
        parser_user.add_argument('user_name', type=str, location='args', required=False)
        args = parser_user.parse_args(strict=True)
        user_name = args.get('user_name')
        print (user_name)
        lstfolder = FolderModel.get_by_user(user_name)
        if lstfolder:
            return {'Data': [folder.json() for folder in lstfolder], 'TotalRows': len(lstfolder), 'Status': 1}
        return {'msg': 'Không tìm thấy thư mục', 'Status': 0}

class FolderByName(Resource):

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('folder_name', type=str, location='args', required=False)
        args = parser.parse_args(strict=False)
        name = args.get('folder_name')
        print (name)
        folder = FolderModel.get_by_name(name)
        if folder:
            return json.dumps({'Data': folder.json(), 'TotalRows': 1, 'Status': 1}, sort_keys=True, indent=True)
        return {'msg': 'Không tìm thấy thư mục', 'Status': 0}



