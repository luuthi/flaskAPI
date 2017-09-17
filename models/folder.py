from db import db


class FolderModel(db.Model):
    __tablename__ = 'folder'

    folder_id = db.Column(db.Integer, primary_key = True)
    folder_name = db.Column(db.String(100))
    user_name = db.Column(db.String(100), db.ForeignKey('user.user_name'))
    created_date = db.Column(db.Datetime)
    folder_type = db.Column(db.Boolean)
    surveys = db.relationship('SurveyModel', lazy ='dynamic',backref='folder')

    def __init__(self,folder_name,username,created_date,folder_type):
        self.folder_name = folder_name
        self.username = username
        self.created_date = created_date
        self.folder_type = folder_type

    def json(self):
        return {'id': self.folder_id, 'folder_name': self.folder_name, 'created_date': self.created_date,
                'folder_type' : self.folder_type, 'user_name': self.user_name,
                'surveys': [survey.json() for survey in self.surveys.all()]}

    @classmethod
    def get_by_id(cls,_folder_id):
        return cls.query.filter_by(folder_id = _folder_id).first()
    
    @classmethod
    def get_by_name(cls,_folder_name):
        return cls.query.filter_by(folder_name = _folder_name).first()

    @classmethod
    def get_by_user(cls,_user_name):
        return cls.query.filter_by(user_name = _user_name).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
