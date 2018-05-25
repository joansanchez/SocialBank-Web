from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
# DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://vagrant:vagrant@localhost:5432/vagrant'
db = SQLAlchemy(app)


class User(db.Model):
    email = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    enabled = db.Column(db.Boolean)
    verified_account = db.Column(db.Boolean)

    def toJSON(self):
        return {'email': self.email,
                'name': self.name,
                'surname': self.surname,
                'enabled': self.enabled,
                'verified': self.verified_account}


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([user.toJSON() for user in users])


@app.route('/users/<email>/verified', methods=['POST'])
def verify_user(email):
    user = User.query.filter_by(email=email).first()
    user.verified_account = True
    db.session.commit()
    return jsonify(''), 204


@app.route('/users/<email>/banned', methods=['POST'])
def ban_user(email):
    user = User.query.filter_by(email=email).first()
    user.enabled = False
    db.session.commit()
    return jsonify(''), 204


if __name__ == '__main__':
    app.run()