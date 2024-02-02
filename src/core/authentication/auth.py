import flask
from flask.helpers import make_response
from flask import views, abort, request, current_app
from core.database import models
from core.database.database import db


class HeartbeatView(views.MethodView):

    def get() -> flask.Response:
        response = make_response("I'm alive", 200)
        response.mimetype = "text/plain"
        return response 


class LoginView(views.MethodView):

    def post() -> dict:
        request_body = flask.request.get_json()

        for field in ("password", "email"):
            if not request_body.get(field, None):
                abort(400, f"Missing field: {field}")
        
        user = models.User.query.filter_by(email=request_body.get('email')).first()
        if not user:
            return {"payload": {"result": "User not found"}, "status_code": 404}
        if not user.verify_password(request_body.get("password")):
            return {"payload": {"result": "Invalid Credentials"}, "status_code": 404}
        auth_token = user.encode_auth_token(user.id)
        if auth_token:
            return {"payload": {"result": {"token" : auth_token}}, "status_code": 200}
        return {"payload": {"result": "Error login !"}, "status_code": 400}


class RegisterView(views.MethodView):

    def post() -> dict:
        request_body = flask.request.get_json()
        for field in ("name", "email", "password"):
            if not request_body.get(field, None):
                abort(400, f"Missing field: {field}")
        
        user = models.User.query.filter_by(email=request_body.get('email')).first()
        if user:
            return {"payload": {"result": "User Already Exist!"}, "status_code": 400}

        user = models.User(
            name=request_body.get("name"),
            email=request_body.get("email")
        )
        user.password = request_body.get("password")
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)

        return {"payload": {"result": {"token" : auth_token}}, "status_code": 201}