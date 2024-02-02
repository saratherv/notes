import flask
from flask import views, abort, request, current_app
from core.database import models
from core.database.database import db
from core.utils.wrapper import requires_jwt_authentication

class UsersView(views.MethodView):

    @requires_jwt_authentication
    def get(user_id: str) -> dict:
        query = db.session.query(models.User).filter(models.User.id == user_id)
        return {
            "payload": {
                "result": [row.dict() for row in query.all()]
            },
            "status_code": 200,
        }
    
    @requires_jwt_authentication
    def post(user_id: str) -> dict:
        request_body = flask.request.get_json()
        for field in ("name", "email"):
            if not request_body.get(field, None):
                abort(400, f"Missing field: {field}")
        user = models.User(
            name=request_body.get("name"),
            email=request_body.get("email")
        )
        db.session.add(user)
        db.session.commit()
        return {"payload": {"result": user.dict()}, "status_code": 201}

class UsersDetailedView(views.MethodView):

    @requires_jwt_authentication
    def get(user_id: str) -> dict:
        query = db.session.query(models.User).filter(models.User.id == user_id)
        result = query.all()
        if not result:
            abort(404, "Record not found")
        if len(result) != 1:
            abort(500, f"Multiple records found {len(result)} when there should only be 1.")

        return {"payload": {"result": result[0].dict()}, "status_code": 200}
    
    def put(item_id: str) -> dict:
        return {}
    
    def delete(item_id: str) -> dict:
        return {}