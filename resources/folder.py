from flask import Flask,request,jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT,jwt_required
from models.folder import FolderModel

class Folder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('folder_name',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('user_name',
        type = str,
        required = True,
        help = "A folder must belong to a user"
    )
    parser.add_argument('created_date',
        type = str,
        required = False
    )
    parser.add_argument('folder_type',
        type = bool,
        required = True,
        help ="This fiield cannot be blank"
    )
    @jwt_required()
    def get(self,name):
        folder = FolderModel.get_by_name(name)
        if folder:
            return folder.json()
        return {'msg':'Store not found'}
    @jwt_required()
    def post(self):
        data = FolderModel.parser.parse_args()
        if FolderModel.get_by_name(data['folder_name']):
            return {'msg','An folder with name {} already exist'.format(data['folder_name'])},404

        folder = FolderModel(**data)
        try:
            folder.save_to_db()
        except:
            return {'msg':'An error occcur in process'},500

        return folder.json(),201
    @jwt_required()
    def put(self, _id):
        data = FolderModel.parser.parse_args()
        folder = FolderModel.get_by_id(_id)
        if folder:
            if FolderModel.get_by_name(data['folder_name']):
                return {'msg','An folder with name {} already exist'.format(data['folder_name'])},404

            folder.folder_name = data['folder_name']
            folder.folder_type = data['folder_type']

            try:
                folder.save_to_db()
            except:
                return {'msg':'An error occcur in process'},500

            return folder.json()
        else:
            return {'msg','Folder not found'},404

    @jwt_required()
    def delete(self,_id):    
        folder = FolderModel.get_by_id(_id)

        if folder:
            folder.delete_from_db()

        return {'msg':'Folder deleted'}
class FolderList(Resource):
    @jwt_required()
    def get(self):
        return {'folders': [folder.json() for folder in FolderModel.query.all()]}