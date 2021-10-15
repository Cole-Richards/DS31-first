import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Determine and returns which user is more likely to say a given tweet
    """
    # Grabbing user from our DB
    # The user we want to compare has to be in our DB
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    # Grabbing tweet vectors from each tweet for each user
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Vertically stack tweet_vects to get one np array
    vects = np.vstack([user0_vects, user1_vects])
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    # fit the model with our x's == vects & our y's == labels
    log_reg = LogisticRegression().fit(vects, labels)

    # vectorize the hypothetical tweet to pass into .predict()
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    return log_reg.predict(hypo_tweet_vect.reshape(1, -1))

#     """Prediction of Users based on Tweet embeddings."""
# import numpy as np
# from sklearn.linear_model import LogisticRegression
# from .models import User
# from .twitter import vectorize_tweet
# from sklearn.metrics import accuracy_score

# def predict_user(user1_name, user2_name, tweet_text):
#     """
#     Determine and return which user is more likely to say a given Tweet.
#     Example run: predict_user('austen', 'elonmusk', 'Lambda School rocks!')
#     Returns 1 (corresponding to first user passed in) or 0 (second).
#     """
#     user0 = User.query.filter(User.name == user0_name).one()
#     user1 = User.query.filter(User.name == user1_name).one()
#     user0_vects = np.array([tweet.vect for tweet in user1.tweets])
#     user1_vects = np.array([tweet.vect for tweet in user2.tweets])
#     embeddings = np.vstack([user1_embeddings, user2_embeddings])
#     labels = np.concatenate([np.ones(len(user1.tweets)),
#                              np.zeros(len(user2.tweets))])
#     log_reg = LogisticRegression().fit(embeddings, labels)
#     # We've done our data science! Now to predict
#     tweet_embedding = vectorize_tweet(tweet_text).reshape(1,-1)
#     y_pred = log_reg.predict(tweet_embedding)
#     y_pred_proba = log_reg.predict_proba(tweet_embedding)
#     #ac_score = log_reg.score(embeddings,y_pred)
#     return y_pred, y_pred_proba