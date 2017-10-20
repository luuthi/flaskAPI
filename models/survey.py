from db import db
from sqlalchemy import func
from models.folder import FolderModel


class SurveyModel(db.Model):

    __tablename__ = 'survey'

    survey_id = db.Column(db.Integer, primary_key=True)
    survey_code = db.Column(db.String(100), unique=True)
    survey_title = db.Column(db.String(500), unique=False)
    survey_desc = db.Column(db.String(1000))
    survey_img = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_date = db.Column(db.Date)
    last_edited = db.Column(db.Date)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.folder_id'))
    user_name = db.Column(db.String(100), db.ForeignKey('users.username'))

    def __init__(self, survey_code, survey_title, survey_desc, survey_img, start_date, end_date,
                 created_date, last_edited, folder_id, user_name):
        self.survey_code = survey_code
        self.survey_title = survey_title
        self.survey_desc = survey_desc
        self.folder_id = folder_id
        self.survey_img = survey_img
        self.start_date = start_date
        self.end_date = end_date
        self.created_date = created_date
        self.last_edited = last_edited
        self.user_name = user_name

    def date_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError

    def json(self):
        return {'survey_id': self.survey_id, 'survey_code': self.survey_code, 'survey_title': self.survey_title,
                'survey_desc': self.survey_desc, 'survey_img': self.survey_img, 'start_date': self.start_date.isoformat(),
                'end_date': self.end_date.isoformat(), 'created_date': self.created_date.isoformat(),
                'last_edited': self.last_edited.isoformat(), 'folder_id': self.folder_id, 'user_name': self.user_name}

    @classmethod
    def get_by_folder(cls, _folder_id, _user_name):
        return cls.query.filter_by(folder_id=_folder_id).filter_by(user_name=_user_name)\
            .order_by(SurveyModel.created_date).all()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(survey_id=_id).first()

    @classmethod
    def get_by_code(cls, _code):
        return cls.query.filter_by(folder_code=_code).first()

    @classmethod
    def get_by_user(cls, _user_name):
        return cls.query.filter_by(user_name=_user_name).order_by(SurveyModel.created_date).all()

    @classmethod
    def get_by_name(cls, _folder_name, _folder_id):
        return cls.query.filter(SurveyModel.survey_title.like('%' + _folder_name + '%'))\
            .filter_by(folder_id=_folder_id).order_by(SurveyModel.created_date).all()

    @classmethod
    def get_max(cls,_user_name):
        print (_user_name)
        return db.session.query(func.max(SurveyModel.survey_id)).filter_by(user_name=_user_name).scalar()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

