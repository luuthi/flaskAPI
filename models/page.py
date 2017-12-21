from db import db

class PageModel(db.Model):

    __tablename__ = 'page'

    page_id = db.Column(db.Integer, primary_key=True)
    page_title = db.Column(db.String(200))
    page_ordered = db.Column(db.Integer)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.survey_id'))


    def __init__(self, page_title, page_ordered, survey_id):
        self.page_title = page_title
        self.page_ordered = page_ordered
        self.survey_id = survey_id

    def json(self):
        return {'page_id': self.page_id, 'page_title': self.page_title, 'page_ordered': self.page_ordered,
        'survey_id': self.survey_id}

    @classmethod
    def get_by_survey(cls, _survey_id):
        return cls.query.filter_by(survey_id=_survey_id).order_by(PageModel.page_ordered).all()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(page_id=_id).first()

    def save_to_db(self):
        print self.json()
        db.session.add(self)
        db.session.commit()
        nid = self.page_id
        return nid

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()