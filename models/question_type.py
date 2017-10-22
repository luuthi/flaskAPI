from db import db
from sqlalchemy import func


class QuestionTypeModel(db.Model):

    __tablename__  = 'questiontype'

    questiontype_id = db.Column(db.Integer, primary_key=True)
    questiontype_name = db.Column(db.String(100), unique=True)
    questiontype_desc = db.Column(db.String(100))
    questiontype_code = db.Column(db.String(10))
    questiontype_status = db.Column(db.Boolean)

    def __init__(self, questiontype_name, questiontype_desc, questiontype_code,questiontype_status):
        self.questiontype_name = questiontype_name
        self.questiontype_code = questiontype_code
        self.questiontype_desc = questiontype_desc
        self.questiontype_status = questiontype_status

    def json(self):
        return {'questiontype_id': self.questiontype_id, 'questiontype_name': self.questiontype_name,
                'questiontype_code': self.questiontype_code, 'questiontype_desc': self.questiontype_desc}

    @classmethod
    def get_all(cls):
        return cls.query.filter_by(questiontype_status=1).all()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(questiontype_id=_id).filter_by(questiontype_status=1).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()