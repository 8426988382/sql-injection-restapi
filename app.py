import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.user import UserRegister, UserLogin
from resources.card import Card
from db import db

uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)  # for cross platform interaction
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserRegister, '/user/register')
api.add_resource(Card, '/card/<string:username>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    app.run(debug=True)
