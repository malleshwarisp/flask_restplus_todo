from base64 import b64decode
from functools import wraps
from typing import List

from db import get_db
from flask.globals import request

from .db_utils import get_user_by_name
from .password_hash import check_password
from .permissions import Permission


def authentication(permissions: List[Permission]):
    def inner(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if "Authorization" in request.headers:
                auth = request.headers["Authorization"]
                auth_parts = b64decode(auth.split(" ")[1]).decode().split(":")
                user = get_user_by_name(get_db(), auth_parts[0])
                if not user:
                    return {"message": "Unauthorized"}, 401
                if not check_password(auth_parts[1], user[2]):
                    return {"message": "Unauthorized"}, 401
                for permission in permissions:
                    if user[3] & permission.value != permission.value:
                        return {"message": "Invalid Permissions"}, 401

                return f(*args, **kwargs)
            else:
                return {"message": "Unauthorized"}, 401

        return decorated

    return inner
