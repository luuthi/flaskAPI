from db import db
from sqlalchemy import func
from models.question_type import QuestionTypeModel
from datetime import datetime


class QuestionModel(db.Model):
    __tablename__ = 'question'

    question_id = db.Column(db.Integer, primary_key=True)
    questiontype_id = db.Column(db.Integer, db.ForeignKey('questiontype.questiontype_id'))
    page_id = db.Column(db.Integer, db.ForeignKey('page.page_id'))
    content = db.Column(db.String(500))
    question_ordred = db.Column(db.Integer)
    question_img = db.Column(db.String(100))
    is_required = db.Column(db.Boolean)
    question_status = db.Column(db.Integer)
    last_edited = db.Column(db.Date)


    def __init__(self, questiontype_id, page_id, content, question_ordered, question_img,
                 is_required, question_status, last_edited):
        self.questiontype_id = questiontype_id
        self.page_id = page_id
        self.content = content
        self.question_ordred = question_ordered
        self.question_img = question_img
        self.is_required = is_required
        self.question_status = question_status
        self.last_edited = last_edited


    def json(self):
        return {'question_id': self.question_id, 'questiontype_id': self.questiontype_id,
                'page_id': self.page_id, 'content': self.content, 'question_ordered': self.question_ordred,
                'question_img': self.question_img, 'is_required': self.is_required,
                'question_status': self.question_status, 'last_edited': self.last_edited.isoformat()}

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(question_id=_id).first()

    @classmethod
    def get_by_page(cls, _page_id):
        return db.session.query(QuestionModel, QuestionTypeModel).\
            join(QuestionTypeModel).add_columns(QuestionModel.question_id,
                                               QuestionModel.questiontype_id,
                                               QuestionModel.question_status,
                                               QuestionModel.question_ordred,
                                               QuestionModel.question_img,
                                               QuestionModel.content,
                                               QuestionModel.page_id,
                                               QuestionModel.is_required,
                                               QuestionModel.last_edited,
                                               QuestionTypeModel.questiontype_code,
                                               QuestionTypeModel.questiontype_name).filter\
                (QuestionTypeModel.questiontype_id == QuestionModel.questiontype_id).filter(QuestionModel.page_id==_page_id).\
                filter(QuestionModel.question_status==True).order_by(QuestionModel.question_ordred.asc()).all()
    @classmethod
    def get_max_ordered(cls, page_id):
        print page_id
        return db.session.query(func.max(QuestionModel.question_ordred)).filter_by(page_id = page_id).scalar()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        nid = self.question_id
        return nid

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




