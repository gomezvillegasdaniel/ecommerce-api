from flask_restful import Resource, reqparse
from models.user_model import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="username field cannot be blank"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="password cannot be blank"
    )
    parser.add_argument('role',
        type=str,
        required=True,
        help="role cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "That username already exists"}, 400

        user = UserModel(data['username'], data['password'], data['role'])
        user.save_to_db()

        return {"message": "User created successfully"}, 201
