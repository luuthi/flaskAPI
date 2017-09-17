from db import db


class SurveyModel(db.Model):
    __tablename__ = 'survey'
    survey_id = db.Column(db.String(80), primary_key=True)
    survey_title = db.Column(db.String(100))
    survey_desc = db.Column(db.String(100))
    survey_img = db.Column(db.String(200))
    start_date = db.Column(db.Datetime)
    end_date = db.Column(db.Datetime)
    created_date = db.Column(db.Datetime)
    last_edited = db.Column(db.Datetime)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.folder_id'))

    def __init__(self, survey_id, survey_title, survey_desc, survey_img, start_date,
                 end_date, created_date, last_edited, folder_id):
        self.survey_id = survey_id
        self.survey_title = survey_title
        self.survey_desc = survey_desc
        self.survey_img = survey_img
        self.start_date = start_date
        self.end_date = end_date
        self.created_date = created_date
        self.last_edited = last_edited
        self.folder_id = folder_id

    def json(self):
        return {'id': self.id,  'name': self.name,'price': self.price}

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
