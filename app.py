import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister
from resources.card import Card
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)  # for cross platform interaction
app.secret_key = '1234addfdg'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(UserRegister, '/user/register')
api.add_resource(Card, '/card/<string:username>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, port=5000)
