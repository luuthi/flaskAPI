# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('fullname',
        type= unicode,
        required = False,
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
        help = "This filed cannot be blank"
    )
    parser.add_argument('user_status',
        type = bool,
        required = True,
        help = "This field cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args(strict=True)
        print(data)
        if UserModel.get_by_username(data['username']):
            return {'msg': 'Đã tồn tại tài khoản với username này', 'status:': '0'}
        if UserModel.get_by_email(data['email']):
            return {'msg': 'Đã tồn tại tài khoản với email này', 'status': '0'}

        user = UserModel(**data)
        newid = 0
        try:
            newid = user.save_to_db()
        except:
            return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}
        return {'msg': 'User created successfully', 'status': '1', 'insertedId': newid}, 201

#