from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT,jwt_required
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
        type= str,
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
    def get(self,_id):
        user =  UserModel.get_by_id(_id)
        if user:
            return user.json(),200
        else:
            return {'msg', 'User not found'}

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.get_by_username(data['username']):
            return {'msg': 'A user with this username already exist'}, 400
        if UserModel.get_by_email(data['email']):
            return {'msg': 'A user with this email already exist'}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {'msg': 'User created successfully'}, 201

    @jwt_required()
    def put(self,_id):
        data = UserRegister.parser.parse_args()
        update_user = UserModel.get_by_id(_id)
        if update_user:
            update_user.full_name = data['full_name']
            update_user.image = data['image']

            update_user.save_to_db()
            return {'msg': 'User updated successfully'}
        else:
            return {'msg': 'User with name {} not exists'.format(data['username'])}, 404

    @jwt_required()
    def delete(self,_id):
        delete_user = UserModel.get_by_id(_id)
        if delete_user:
            delete_user.delete_from_db()
        else:
            return {'msg': 'User not found'}, 404
        return {'msg': 'User deleted'}


class UserList(Resource):
    @jwt_required()
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all().order_by(UserModel.user_id)]}, 200