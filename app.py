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
#postgres://qpdggmnrmhrsim:7452f8111d18456b355d432280661f87eacc3c5236c8ca1f55be3b861bb55127@ec2-54-225-237-64.compute-1.amazonaws.com:5432/d4i7ve72ue4i15
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://qpdggmnrmhrsim:7452f8111d18456b355d432280661f87eacc3c5236c8ca1f55be3b861bb55127@ec2-54-225-237-64.compute-1.amazonaws.com:5432/d4i7ve72ue4i15')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'thild'
api = Api(app)



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
