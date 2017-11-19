from db import db

class ChoiceModel(db.Model):
    __tablename__ = 'Choice'

    choice_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    choice_ordered = db.Column(db.Integer)
    choice_value = db.Column(db.String(500))
    choice_content = db.Column(db.String(500))
    last_edited = db.Column(db.Date)

    def __init__(self, question_id, choice_ordered, choice_value, choice_content, last_edited):
        self.question_id = question_id
        self.choice_ordered = choice_ordered
        self.choice_content =choice_content
        self.choice_value = choice_value
        self.last_edited = last_edited

    def date_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError

    def json(self):
        return {'choice_id' : self.choice_id, 'question_id': self.question_id, 'choice_ordered': self.choice_ordered,
                 'choice_content': self.choice_content, 'last_edited': self.last_edited.isoformat()}

    @classmethod
    def get_by_id(cls, _id):
        return  cls.query.filter_by(choice_id=_id).first()

    @classmethod
    def get_by_question(cls, _id):
        return cls.query.filter_by(question_id=_id).order_by(ChoiceModel.choice_ordered).order_by(ChoiceModel.choice_ordered.asc()).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()