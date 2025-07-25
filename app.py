from flask import Flask, render_template, jsonify, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)
Session(app)

class UserCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=105)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users/count')
def get_count():
    user_count = UserCount.query.first()
    if not user_count:
        user_count = UserCount(count=105)
        db.session.add(user_count)
        db.session.commit()
        session['prev_count'] = 105
    else:
        user_count.count += 1
        db.session.commit()

    prev = session.get('prev_count', user_count.count)
    if user_count.count > prev:
        flash(f'User count increased to {user_count.count}')
        session['prev_count'] = user_count.count

    return jsonify({'count': user_count.count})

if __name__ == '__main__':
    app.run(debug=True)
