import flask
from flask import views, abort
from core.database import models
from core.database.database import db
from core.utils.wrapper import requires_jwt_authentication


class NotesHistoryView(views.MethodView):

    @requires_jwt_authentication
    def get(user_id: str) -> dict:
        query = db.session.query(models.NotesHistory)

        if "note_id" in flask.request.args:
            # Filter by note id
            note = db.session.query(models.Notes).get(flask.request.args.get("note_id"))
            if not note:
                abort(404, "Invalid note ID")
            query = query.filter(models.Notes.id == flask.request.args.get("note_id"))
        
        return {
            "payload": {
                "result": [row.dict() for row in query.all()]
            },
            "status_code": 200,
        }