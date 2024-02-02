import json
import os
from datetime import datetime, timedelta
from uuid import uuid4
from flask import current_app
# from sqlalchemy import func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.mysql import LONGTEXT
import jwt
from .database import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(256), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, onupdate=datetime.utcnow())

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError("password is not a readable attribute.")

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def join_criterion() -> dict:
        return {}

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name})"

    @staticmethod
    def dict_keys() -> tuple:
        return ("id", "name", "email", "created_at", "last_updated")
    
    def dict(self, columns: tuple = None):
        return self.to_dict(only=columns if columns else self.dict_keys())
    
    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
                'iat': datetime.utcnow(),
                'sub': "sub_" + str(user_id)
            }
            return jwt.encode(
                payload,
                current_app.config.get("SECRET_KEY"),
                algorithm='HS256'
            )
        except Exception as e:
            return e
        
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY") , algorithms=["HS256"])
            if payload and "sub" in payload:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Notes(db.Model, SerializerMixin):

    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(LONGTEXT)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, onupdate=datetime.utcnow())

    @staticmethod
    def join_criterion() -> dict:
        return {
            "User" : (User, User.id == Notes.user_id),
        }

    def __repr__(self) -> str:
        return f"Note(id={self.id}, name={self.title})"

    @staticmethod
    def dict_keys() -> tuple:
        return ("id", "title", "description", "user_id", "created_at", "last_updated")
    
    def dict(self, columns: tuple = None):
        return self.to_dict(only=columns if columns else self.dict_keys())
    
class NotesHistory(db.Model, SerializerMixin):

    __tablename__ = "notes_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(128), nullable=True)
    description = db.Column(LONGTEXT)
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    @staticmethod
    def join_criterion() -> dict:
        return {
            "Notes" : (Notes, Notes.id == NotesHistory.note_id),
        }

    def __repr__(self) -> str:
        return f"Note(id={self.id}, name={self.title})"

    @staticmethod
    def dict_keys() -> tuple:
        return ("id", "title", "description", "note_id", "created_at")
    
    def dict(self, columns: tuple = None):
        return self.to_dict(only=columns if columns else self.dict_keys())


