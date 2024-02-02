import flask
from flask import views, abort
from sqlalchemy.sql import null
from core.database import models
from core.database.database import db
from core.utils.wrapper import requires_jwt_authentication


class NotesView(views.MethodView):

    @requires_jwt_authentication
    def get(user_id: str) -> dict:
        query = db.session.query(models.Notes).filter(models.Notes.user_id == user_id)
        
        return {
            "payload": {
                "result": [row.dict() for row in query.all()]
            },
            "status_code": 200,
        }

    @requires_jwt_authentication
    def post(user_id: str) -> dict:
        request_body = flask.request.get_json()
        request_body["user_id"] = 1
        for field in ("title", "description"):
            if not request_body.get(field, None):
                abort(400, f"Missing field: {field}")

        note = models.Notes(
            title=request_body.get("title"),
            description=request_body.get("description"),
            user_id=user_id
        )    
        db.session.add(note)
        db.session.commit()
        return {"payload": {"result": note.dict()}, "status_code": 201}

class NotesDetailedView(views.MethodView):

    @requires_jwt_authentication
    def get(note_id: str, user_id: str) -> dict:
        query = db.session.query(models.Notes).filter(models.Notes.id == note_id)
        result = query.all()
        if not result:
            abort(404, "Record not found")
        if len(result) != 1:
            abort(500, f"Multiple records found {len(result)} when there should only be 1.")

        return {"payload": {"result": result[0].dict()}, "status_code": 200}
    
    @requires_jwt_authentication
    def put(note_id: str, user_id: str) -> dict:
        note = db.session.query(models.Notes).get(note_id)
        if not note:
            abort(404, "Note not found")
        request_body = flask.request.get_json()
        changed = False
        old_title, old_description = null(), null()
        if "title" in request_body:
            old_title = note.title
            note.title = request_body.get("title")
            changed = True
        if "description" in request_body:
            old_description = note.description
            note.description = request_body.get("description")
            changed = True
        if changed:
            old_note = models.NotesHistory(
                title=old_title,
                description=old_description,
                note_id=note_id
            )    
            db.session.add(old_note)
            db.session.commit()

        return {
            "payload": {"result": note.dict()},
            "status_code": 200,
        }
    
    @requires_jwt_authentication
    def delete(note_id: str, user_id:str) -> dict:
        note = db.session.query(models.Notes).get(note_id)
        if not note:
            abort(404, f"Note at ID: {note_id} not found")

        db.session.query(models.Notes).filter(models.Notes.id == note_id).delete()
        db.session.commit()
        return {
            "payload": {"result": "Note deleted"},
            "status_code": 200,
        }