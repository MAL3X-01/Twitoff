'''Retrieve Tweets, embeddings, and persist in the database.'''
import tweepy
import basilica
from decouple import config
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('twitter_consumer_key'),
                                   config('twitter_consumer_secret'))
TWITTER_AUTH.set_access_token(config('twitter_token'),
                              config('twitter_token_secret'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('basilica_key'))


def add_or_update_user(username):
    '''Add or update a user *and* their Tweets, error if no/private user'''
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        # we want as many recent non-retweet/reply statuses as we can get
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            # get embedding for tweet, and store in db
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')
            db_tweet = Tweet(id=tweet.id, full_text=tweet.full_text[:500],
                             embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()
