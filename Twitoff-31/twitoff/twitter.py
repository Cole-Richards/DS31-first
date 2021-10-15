"""Getting tweets and users from the Twitter DB"""
from os import getenv
import tweepy
import spacy
from tweepy import auth
from .models import User, db, Tweet

auth = tweepy.OAuthHandler(
    getenv("TWITTER_API_KEY"),
    getenv("TWITTER_API_KEY_SECRET")
)
twitter = tweepy.API(auth)


# loads word2vect Model
nlp = spacy.load("my_nlp_model")


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    """
    Gets twitter user and tweets from twitter DB
    Gets user by "username" parameter.
    """
    try:
        # gets back twitter user object
        twitter_user = twitter.get_user(screen_name = username)
        # Either updates or adds user to our DB
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)
        db.session.add(db_user)  # Add user if don't exist

        # Grabbing tweets from "twitter_user"
        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id
        )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # tweets is a list of tweet objects
        for tweet in tweets:
            # type(tweet) == object
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(
                id=tweet.id,
                text=tweet.full_text,
                vect=tweet_vector
            )
            db_user.tweets.append(db_tweet)
            db.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else:
        db.session.commit()