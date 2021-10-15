from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#creates a user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # id as primar key
    name = db.Column(db.String(50), nullable=False)
    #user name
    newest_tweet_id = db.Column(db.Integer)
    

    def __repr__(self):
        return "<User: {}>".format(self.name)

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # Num of tweets as primary key
    text = db.Column(db.Text, nullable=False)
    #tweet
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))
    vect = db.Column(db.PickleType, nullable=False)
    
    def __repr__(self):
        return "<Tweet: {}>". format(self.text)

CREATE_USER_TABLE_SQL = """
    CREATE TABLE IF NOT EXIST user (
        id INT PRIMARY,
        name STRING NOT NULL
    );

"""