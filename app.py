import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.register import UserRegister

app = Flask(__name__)
app.config['DEBUG'] = True
#sqlite:///data.db
#postgres://zyqfvsqtqnnjlt:37e8daf153bb33265bfdcbf8a7
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://zyqfvsqtqnnjlt:37e8daf153bb33265bfdcbf8a7')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_ENABLED'] = True
app.secret_key = 'thild'
api = Api(app)
CORS(app, origins="http://localhost:4200", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True)
CORS(app)


jwt = JWT(app, authenticate, identity) #/auth

# api.add_resource(Item,'/item/<string:name>')
# api.add_resource(ItemList,'/items')
api.add_resource(UserRegister, '/register')
# api.add_resource(Store,'/store/<string:name>')
# api.add_resource(StoreList,'/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
