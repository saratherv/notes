import json
import os
from datetime import datetime
from uuid import uuid4

# from sqlalchemy import func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import aliased

from .database import db

class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(256), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, onupdate=datetime.utcnow())

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