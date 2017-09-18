from db import db


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=False)
    fullname = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(100), unique=True)
    image = db.Column(db.String(200), unique=False)
    user_type = db.Column(db.Boolean, unique=False)
    user_status = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, username, password, fullname, email, image, user_type, user_status):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.email = email
        self.image = image
        self.user_type = user_type
        self.user_status = user_status

    def json(self):
        return {'id': self.id, 'username': self.username, 'fullname': self.fullname,
                'email': self.email, 'image': self.image, 'user_status': self.user_status, 'user_type': self.user_type}

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(user_id=_id).first()
    
    @classmethod
    def get_by_email(cls, _email):
        return cls.query.filter_by(email=_email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
  