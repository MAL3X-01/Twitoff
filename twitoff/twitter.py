'''Retrieve Tweets, embeddings, and persist in the database.'''
import tweepy, basilica
from decouple import config
from .module import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('twitter_consumer_key'),
                                   config('twitter_consumer_secret'))
TWITTER_AUTH.set_access_token(config('twitter_token'),
                              config('twitter_token_secret'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('basilica_key'))
#embedding = conn.embed_sentence('hey this is a cool tweet', model='twitter')
