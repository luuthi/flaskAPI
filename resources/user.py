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
        help = "This filed cannot be blank"
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
        print (data)
        update_user = UserModel.get_by_id(_id)
        if update_user:
            update_user.full_name = data['fullname']
            update_user.image = data['image']

            update_user.save_to_db()
            return {'msg': 'User updated successfully'}
        else:
            return {'msg': 'User with name {} not exists'.format(data['username'])}, 404

class UserByName(Resource):
    def get(self, username):
        user = UserModel.get_by_username(username)
        if user:
            return { 'Data': user.json(), 'Status' :1}, 200
        else:
            return {'msg': 'User not found', 'Status': 0}