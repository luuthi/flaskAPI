from db import db

class QuestionTypeModel(db.Model):
    __table__ = 'question_type'
    questiontype_id = db.Column(db.Integer, primary_key = True)
    questiontype_name = db.Column(db.String(100),unique = True)
    questiontype_desc = db.Column(db.String(100))
    questiontype_code = db.Column(db.String(20))

    questions = db.relationship('QuestionModel', lazy = 'dynamic', backref='questiontype')

    def __init__(self, _id,_name,_desc,_code):
        self.questiontype_id = _id
        self.questiontype_name = _name
        self.questiontype_code = _code
        self.questiontype_desc = _desc

    def json(self):
        return {'questiontype_id': self.questiontype_id, 'questiontype_name': self.questiontype_name,'questiontype_desc': self.questiontype_desc, 'questiontype_code': self.questiontype_code}

    @classmethod
    def get_by_code(cls,_code):
        return cls.query.filter_by(questiontype_code = _code).first()

    @classmethod
    def get_by_id(cls,_id):
        return cls.query.filter_by(questiontype_id = _id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()