# -*- encoding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.user import UserModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=False
    )
    parser.add_argument('fullname',
        type= unicode,
        required = True,
        help = "This field cannot be blank"
    )
    parser.add_argument('email',
        type = str,
        required = True,
        help="This field cannot be blank"
    )
    parser.add_argument('image',
        type = str,
        required = False,
        help = ""
    )
    parser.add_argument('user_type',
        type = bool,
        required = True,
        help = "This field cannot be blank"
    )
    parser.add_argument('user_status',
        type = bool,
        required = True,
        help = "This field cannot be blank"
    )

    @jwt_required()
    def get(self, _id):
        user = UserModel.get_by_id(_id)
        if user:
            return {'Data': user.json(), 'Status': 1}, 200
        else:
            return {'msg': 'User not found', 'Status': 0}


    @jwt_required()
    def put(self, _id):
        data = User.parser.parse_args()
        update_user = UserModel.get_by_id(_id)
        if update_user:
            update_user.fullname = data['fullname']
            update_user.image = data['image']
            try :
                update_user.save_to_db()
                return {'msg': 'User updated successfully', 'Status': 1}
            except:
                return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}
        else:
            return {'msg': 'User with name {} not exists'.format(data['username'])}, 404

class UserByName(Resource):
    def get(self, username):
        user = UserModel.get_by_username(username)
        if user:
            return { 'Data': user.json(), 'Status' :1}, 200
        else:
            return {'msg': 'User not found', 'Status': 0}

class UserPassword(Resource):
    @jwt_required()
    def get(self,username):
        password = UserModel.get_password(username)
        if password:
            return {'Data' : password, 'Status': 1}
        else:
            return {'msg': 'User not found', 'Status': 0}

    @jwt_required()
    def put(self, username):
        parser1 = reqparse.RequestParser()
        parser1.add_argument('password',type=str,required=True)
        args = parser1.parse_args(strict=True)
        password = args.get('password')
        update_user = UserModel.get_by_username(username)
        if update_user:
            update_user.password = password
            try:
                update_user.save_to_db()
                return {'msg': 'User updated successfully', 'Status': 1}
            except:
                return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}
        else:
            return {'msg': 'User not exists'}, 404
