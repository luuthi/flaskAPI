from db import db
from sqlalchemy import func


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


    def date_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError

    def json(self):
        return {'question_id': self.question_id, 'questiontype_id': self.questiontype_id,
                'page_id': self.page_id, 'content': self.content, 'question_orderd': self.question_ordred,
                'question_img': self.question_img, 'isrequired': self.is_required,
                'status': self.question_status, 'last_edited': self.last_edited.isoformat()}

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(question_id=_id).first()

    @classmethod
    def get_by_page(cls, _page_id):
        return cls.query.filter_by(page_id=_page_id).filter_by(question_status=True).order_by(QuestionModel.question_ordred).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




