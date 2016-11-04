"""Listens to UCB NYC tweets and sends sms notifications."""

import secrets
import tweepy
import twilio

UCB_NYC_USER_ID = '289051336'
TEST_USER_ID = '109207291'


class SMSListener(tweepy.StreamListener):
    """Tweet listener that can send SMS."""

    def __init__(self):
        super(SMSListener, self).__init__()
        self.twilio_client = twilio.rest.TwilioRestClient(
            secrets.TWILIO_ACCOUNT_SID,
            secrets.TWILIO_AUTH_TOKEN)

    def on_status(self, status):
        """Overrides base class; called when a new tweet is pushed to us."""
        self.send_if_relevant(status.text)

    def send_if_relevant(self, tweet_text):
        print tweet_text
        if self.is_relevant_tweet(tweet_text):
            try:
                message = self.twilio_client.messages.create(
                    body=tweet_text,
                    to=secrets.TO_PHONE_NUMBER,
                    from_=secrets.TWILIO_PHONE_NUMBER)
            except TwilioRestException as e:
                print e

    def is_relevant_tweet(self, text):
        return False


class Improv101Listener(SMSListener):
    """Tweet SMS listener that cares about tweets about improv 101"""

    def is_relevant_tweet(self, text):
        return 'Improv 101' in text


def connect_and_listen():
    auth = tweepy.OAuthHandler(secrets.TWITTER_CONSUMER_KEY, secrets.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(secrets.TWITTER_ACCESS_TOKEN, secrets.TWITTER_ACCESS_TOKEN_SECRET)
    twitter_api = tweepy.API(auth)
    listener = Improv101Listener()
    stream = tweepy.Stream(
        auth=twitter_api.auth,
        listener=listener)

    # Wait for tweets and act on them. This call is syncronous and blocks.
    stream.filter(follow=[TEST_USER_ID])


if __name__ == '__main__':
    connect_and_listen()

