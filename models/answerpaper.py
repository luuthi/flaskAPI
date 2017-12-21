import sqlite3
from db import db

class AnswerPaperModel(db.Model):
    __tablename__ = 'answerpaper'

    answerpaper_id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.String(100))
    created_date = db.Column(db.Date)
    status = db.Column(db.Integer)


    def date_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError

    def __init__(self, survey_id, created_date, status):
        self.survey_id = survey_id
        self.status = status
        self.created_date = created_date

    def json(self):
        return {'answerpaper_id': self.answerpaper_id, 'survey_id': self.survey_id,
                'created_date': self.created_date.isoformat(), 'status': self.status}

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(answerpaper_id=_id).first()

    @classmethod
    def get_by_survey(cls, _id):
        return cls.query.filter_by(survey_id=_id).order_by(AnswerPaperModel.created_date).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        nid = self.answerpaper_id
        return nid

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

