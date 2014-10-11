from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:blabla@localhost/snooze'
db = SQLAlchemy(app)
api = restful.Api(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(500))
    balance = db.Column(db.Integer)

    def __init__(self, email, password, balance=None):
        self.email = email
        self.password = password
        self.balance = balance

    def __repr__(self):
        return '<User %r>' % self.email


class Balance(restful.Resource):
    def get(self):
        user = Users.query.all()[0]
        return {'balance': user.balance}


class Snooze(restful.Resource):
    def post(self):
        user = Users.query.all()[0]
        if user.balance <= 0:
            abort(400, message="Out of money!")
        else:
            user.balance -= 1
            db.session.commit()
        return {'balance': user.balance}


api.add_resource(Balance, '/balance')
api.add_resource(Snooze, '/snooze')

if __name__ == '__main__':
    app.run(debug=True)
