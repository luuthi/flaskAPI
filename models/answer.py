from db import db
from sqlalchemy import text
from models.question import QuestionModel

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
        # return cls.query.filter_by(question_id=_id).all()
        question =  QuestionModel.get_by_id(_id)
        data = []
        if question.questiontype_id == 1 or question.questiontype_id == 3:
            sql = text('select  answer.answer_value, answer.question_id, count(answer.answer_value) answer_count, Choice.choice_content from answer join answerpaper on answer.answerpaper_id = answerpaper.answerpaper_id join Choice on answer.question_id || "_" || Choice.choice_id = answer.answer_value where answerpaper.status = 1 and answer.question_id = %d group by  answer.answer_value, answer.question_id ' % _id )
            result = db.engine.execute(sql)
            if result:
                for r in result:
                    data.append({
                        'question_id' : r['question_id'],
                        'answer_value' : r['answer_value'],
                        'answer_count' : r['answer_count'],
                        'choice_content' : r['choice_content']
                    })
        elif question.questiontype_id == 4:
            sql = text('select substr(answer.answer_value,3) as answer_value, answer.question_id, count(answer.answer_value) answer_count from answer join answerpaper on answer.answerpaper_id = answerpaper.answerpaper_id where answerpaper.status = 1 and answer.question_id = %d group by  answer.answer_value, answer.question_id' % _id)
            result = db.engine.execute(sql)
            if result:
                for r in result:
                    data.append({
                        'question_id': r['question_id'],
                        'answer_value': r['answer_value'],
                        'answer_count': r['answer_count'],
                        'choice_content': ''
                    })
        elif question.questiontype_id == 2:
            sql = text('select question_id,answer_value from answer where answer.question_id = %d' %_id)
            result = db.engine.execute(sql)
            if result:
                for r in result:
                    data.append({
                        'question_id': r['question_id'],
                        'answer_value': r['answer_value']
                    })
        elif question.questiontype_id == 5 or question.questiontype_id == 6 or question.questiontype_id == 7:
            sql = text('select answer.answer_value from answer where answer.question_id = %d and answer.answer_value is not null and answer.answer_value <> ""' % _id)
            result = db.engine.execute(sql)
            if result:
                index = 1
                for r in result:
                    if question.questiontype_id == 6:
                        data.append({
                            'no': index,
                            'answer_value': r['answer_value'].replace("-","/")
                        })
                    elif question.questiontype_id == 7:
                        data.append({
                            'no': index,
                            'answer_value': r['answer_value'].replace("-", ":")
                        })
                    elif question.questiontype_id == 5:
                        data.append({
                            'no': index,
                            'answer_value': r['answer_value']
                        })
                    index = index +1
        return data

    @classmethod
    def get_count_answer_by_question(cls, _qid):
        data = []
        item = {}
        sql = text('SELECT SUM(CASE WHEN answer.answer_value is  null or answer.answer_value == "" THEN 1 ELSE 0 END) as not_answered_number, SUM(CASE WHEN answer.answer_value is not null or answer.answer_value <> "" THEN 1 ELSE 0 END) as answered_number from answer where answer.question_id = %d' % _qid)
        res= db.engine.execute(sql)
        if res:
            for r in res:
                data.append({
                    'answered_number': r['answered_number'],
                    'not_answered_number': r['not_answered_number']
                })
        return data
    @classmethod
    def get_by_ansp(cls, _id):
        return  cls.query.filter_by(question_id=_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()