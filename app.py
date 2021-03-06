import os
import re

from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT,current_identity

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList


#Flask SQLAlchemy doesn`t support postgress DB anymore only postgresql !
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
#os.environ.get('DATABASE_URL_POSTGRES', 'sqlite:///data.db') not working


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
#database_uri =sqlite:///data.db for local runs

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)



jwt = JWT(app, authenticate, identity)  # /auth





api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
