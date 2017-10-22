from db import db

class AnswerModel(db.Model):


    __tablename__ = 'answer'

    answer_id = db.Column(db.Integer, primary_key=True)
    answerpaper_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    answer_value = db.Column(db.String(500))

    def __init__(self, answerpaper_id, question_id, answer_value):
        self.answerpaper_id = answerpaper_id
        self.question_id = question_id
        self.answer_value = answer_value

    def json(self):
        return {'answer_id': self.answer_id, 'answerpaper_id': self.answerpaper_id,
                'question_id': self.question_id, 'answer_value': self.answer_value}

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(answer_id=_id).first()

    @classmethod
    def get_by_question(cls, _id):
        return cls.query.filter_by(question_id=_id).first()

    @classmethod
    def get_by_ansp(cls, _id):
        return  cls.query.filter_by(question_id=_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()