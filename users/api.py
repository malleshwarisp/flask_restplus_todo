from functools import wraps
from flask_restplus import Namespace, Resource, fields

from .permissions import Permission
from .db_utils import *
from .authentication import authentication

api = Namespace("user", description="Users Operations")

user = api.model(
    "User",
    {
        "id": fields.Integer(readonly=True, description="User's unique ID"),
        "username": fields.String(required=True, description="User name"),
        "password": fields.String(required=True, description="User's password"),
        "permission": fields.List(
            fields.String(enum=Permission._member_names_),
            required=True,
            description="User's permissions",
        ),
    },
)

user_list = api.model(
    "UserList",
    {
        "id": fields.Integer(readonly=True, description="User's unique ID"),
        "username": fields.String(required=True, description="User name"),
        "permission": fields.List(
            fields.String(enum=Permission._member_names_),
            required=True,
            description="User's permissions",
        ),
    },
)


@api.route("/")
@api.response(401, "Unauthorized")
class UserList(Resource):
    """Shows a list of all the users and lets you create a new user"""

    @api.doc("list_users", security="Basic Auth")
    @authentication(permissions=[Permission.ADMIN])
    @api.marshal_list_with(user_list)
    def get(self):
        """List all users"""
        users = get_users(get_db())
        return list(map(user_to_dict, users))

    @api.doc("create_user", security="Basic Auth")
    @api.expect(user)
    @authentication(permissions=[Permission.ADMIN])
    @api.marshal_with(user_list)
    def post(self):
        """Create a new User"""
        req = api.payload
        result = create_user(
            get_db(), req["username"], req["password"], req["permission"]
        )
        if not result:
            api.abort(409, "Username already exists")
        return user_to_dict(result)
