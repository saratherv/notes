import flask
from flask import views, abort, request, current_app
from sqlalchemy.sql import null
# from core.database import models
from core.database.database import db

class NotesView(views.MethodView):

    def get() -> dict:
        return {}
    
    def post() -> dict:
        return {}

class NotesDetailedView(views.MethodView):

    def get(item_id: str) -> dict:
        return {}
    
    def put(item_id: str) -> dict:
        return {}
    
    def delete(item_id: str) -> dict:
        return {}