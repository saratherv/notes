import functools
from flask import make_response, request, abort
import jwt
from core.database.models import User

def requires_jwt_authentication(func):
    # @profile
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        
        try:              
            token_header = request.headers['token']
            if token_header:
                resp = User.decode_auth_token(token_header)
                if isinstance(resp, str):
                    user_id = int(resp.split("_")[1])
                    user = User.query.filter_by(id=user_id).first()
                    if user:
                        kwargs["user_id"] = user_id
                        return func(*args, **kwargs)
                    else:
                        abort(400, f"Invalid User ID: {user_id}")

        except Exception as e: 
            return make_response(
                { "result": f"{str(e)}" },
                403
            )
    return wrap