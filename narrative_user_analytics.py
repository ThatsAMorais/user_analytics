from datetime import datetime, timedelta

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'postgresql://narrative:narrative1@db:5432/narrative'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

RETRIEVE_RESPONSE_TEMPLATE = """
unique_users,{number_of_unique_usernames}
clicks,{number_of_clicks}
impressions,{number_of_impressions}
"""


# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(250), primary_key=True)


class Click(db.Model):
    __tablename__ = 'clicks'
    time = db.Column(db.DateTime, primary_key=True)
    user_id = db.Column(db.Text, db.ForeignKey('users.id'))


class Impression(db.Model):
    __tablename__ = 'impressions'
    time = db.Column(db.DateTime, primary_key=True)
    user_id = db.Column(db.Text, db.ForeignKey('users.id'))


def read_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp))
    except (ValueError, OverflowError, OSError):
        return None


# Routes
@app.route('/analytics', methods=['POST'])
def create_analytics(*args, **kwargs):
    timestamp = read_timestamp(request.args.get('timestamp'))
    user = request.args.get('user')
    event = request.args.get('event')

    if timestamp and user:
        existing_user = User.query.get(user)
        if not existing_user:
            db.session.add(User(id=user))
            db.session.commit()

        if event == 'click':
            # store a click
            datum = Click(time=timestamp, user_id=user)
        elif event == 'impression':
            # store an impression
            datum = Impression(time=timestamp, user_id=user)

        if datum:
            db.session.add(datum)
            db.session.commit()

    return ('', 204, [])


@app.route('/analytics', methods=['GET'])
def retrieve_analytics(*args, **kwargs):
    timestamp = read_timestamp(request.args.get('timestamp'))
    from_timestamp = timestamp - timedelta(hours=1)
    
    clicks = db.session.query(Click).filter(
        Click.time.between(from_timestamp, timestamp)
    )
    impressions = db.session.query(Impression).filter(
        Impression.time.between(from_timestamp, timestamp)
    )

    users = dict()
    for click in clicks:
        if click.user_id not in users:
            users[click.user_id] = 1
    for impression in impressions:
        if impression.user_id not in users:
            users[impression.user_id] = 1
    
    if timestamp:
        return RETRIEVE_RESPONSE_TEMPLATE.format(
            number_of_unique_usernames=len(users.keys()),
            number_of_clicks=clicks.count(),
            number_of_impressions=impressions.count(),
        )
    return ('Invalid', 400, [])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
