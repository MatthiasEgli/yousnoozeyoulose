from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import reqparse
import stripe
from flask.ext.cors import CORS
import datetime as dt

app = Flask(__name__)
cors = CORS(app, headers="content-type")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:blabla@localhost/snooze'
stripe.api_key = "sk_test_yAIxmdiXsy9YbLfkFDCUen30"
db = SQLAlchemy(app)
api = restful.Api(app)

cost = 100


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(500))
    balance = db.Column(db.Integer)
    charities = db.relationship('Charities', backref='user',
                                lazy='dynamic')
    transfers = db.relationship('Transfers', backref='user',
                                lazy='dynamic')

    def __init__(self, email, password, balance=None):
        self.email = email
        self.password = password
        self.balance = balance

    def __repr__(self):
        return '<User %r>' % self.email


class Charities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    charity = db.Column(db.String(500))
    time_added = db.Column(db.DateTime)

    transfers = db.relationship('Transfers', backref='charity',
                                lazy='dynamic')

    def __init__(self, userid, charity):
        self.userid = userid
        self.charity = charity
        self.time_added = dt.datetime.utcnow()

    def __repr__(self):
        return '<Charity %r>' % self.charity


class Transfers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    charityid = db.Column(db.Integer, db.ForeignKey('charities.id'))
    amount = db.Column(db.Integer)
    time_added = db.Column(db.DateTime)

    def __init__(self, userid, charityid, amount):
        self.userid = userid
        self.charityid = charityid
        self.amount = amount
        self.time_added = dt.datetime.utcnow()

    def __repr__(self):
        return '<Transfer %r>' % self.id


class Balance(restful.Resource):
    def get(self):
        user = Users.query.all()[0]
        return {'balance': user.balance}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=int, location='json')
        parser.add_argument('token', type=str, location='json')
        args = parser.parse_args()
        user = Users.query.all()[0]

        try:
            stripe.Charge.create(
                amount=args["amount"],
                currency="chf",
                card=args["token"]
            )
            user.balance += args["amount"]
            db.session.commit()
        except stripe.CardError:
            pass

        return {'balance': user.balance}


class Snooze(restful.Resource):
    def get(self):
        user = Users.query.all()[0]
        if user.balance <= 0:
            return {
                'balance': user.balance,
                'cost_last_snooze': 0,
            }
        else:
            current_cost = cost
            for t in user.transfers:
                if t.time_added > dt.datetime.utcnow()-dt.timedelta(minutes=10):
                    current_cost *= 2
            user.balance -= current_cost
            if user.balance < 0:
                current_cost += user.balance
                user.balance = 0
            t = Transfers(
                userid=user.id,
                charityid=user.charities[-1].id,
                amount=current_cost
            )
            user.transfers.append(t)
            db.session.commit()
        return {
            'balance': user.balance,
            'cost_last_snooze': current_cost,
        }


class Charity(restful.Resource):
    def post(self):
        user = Users.query.all()[0]
        parser = reqparse.RequestParser()
        parser.add_argument('charity', type=str, location='json')
        args = parser.parse_args()
        c = Charities(userid=user.id, charity=args["charity"])
        user.charities.append(c)
        db.session.commit()
        return {
            'charity': c.charity
        }

    def get(self):
        user = Users.query.all()[0]
        return {
            'charity': user.charities[-1].charity
        }


class Transfer(restful.Resource):
    def post(self):
        user = Users.query.all()[0]
        parser = reqparse.RequestParser()
        parser.add_argument('charity', type=str, location='json')
        args = parser.parse_args()
        c = Charities(userid=user.id, charity=args["charity"])
        user.charities.append(c)
        db.session.commit()
        return {
            'charity': c.charity
        }

    def get(self):
        user = Users.query.all()[0]
        return {
            'charity': user.charities[-1].charity
        }


api.add_resource(Balance, '/balance')
api.add_resource(Snooze, '/snooze')
api.add_resource(Charity, '/charities')

if __name__ == '__main__':
    app.run(debug=True)
