import sqlite3
from db import db


class FolderModel(db.Model):

    __tablename__ = 'folder'

    folder_id = db.Column(db.Integer, primary_key=True)
    folder_name = db.Column(db.String(100), unique=False)
    user_name = db.Column(db.String(100), db.ForeignKey('users.username'))
    user = db.relationship('UserModel')
    created_date = db.Column(db.Date, unique=False)
    folder_type = db.Column(db.Boolean, unique=False)

    def __init__(self, folder_name, user_name, created_date, folder_type):
        self.folder_name = folder_name
        self.user_name = user_name
        self.created_date = created_date
        self.folder_type = folder_type

    def date_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError
    def json(self):
        return {'id': self.folder_id, 'folder_name': self.folder_name, 'created_date': self.created_date.isoformat(),
                'folder_type' : self.folder_type, 'user_name': self.user_name}


    @classmethod
    def get_by_id(cls, _folder_id):
        return cls.query.filter_by(folder_id=_folder_id).first()
    
    @classmethod
    def get_by_name(cls, _folder_name):
        return cls.query.filter_by(folder_name=_folder_name).first()

    @classmethod
    def get_by_user(cls, _user_name):
        return cls.query.filter_by(user_name=_user_name).order_by(FolderModel.created_date.desc()).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
