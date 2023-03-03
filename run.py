from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask('app')
app.config.from_pyfile('default_config.py')
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config.from_envvar("SQLALCHEMY_DATABASE_URI_ps", silent=True)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
db = SQLAlchemy(app)
app.app_context().push()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(123), unique=True)
    password = db.Column(db.String(123))


# db.drop_all()
db.create_all()


@app.get('/')
def index():
    users = User.query.all()
    response = {
        "total": len(users),
        "users": [{"username": user.username} for user in users],
    }
    return jsonify(response), 200


@app.get('/ping')
def ping():
    return 'pong', 200


@app.post('/register')
def register():
    user_data = request.json
    if not user_data or 'username' not in user_data or 'password' not in user_data:
        return jsonify({"error": "bad request"}), 400

    try:
        user = User(username=user_data['username'], password=user_data['password'])
        db.session.add(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return 'error', 400

    return 'ok', 200

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000)
