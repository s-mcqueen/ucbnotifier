"""Listens to tweets and sends sms notifications."""

# TODO: write tests

import secrets
import tweepy
import twilio

TWILIO_CLIENT = twilio.rest.TwilioRestClient(
    secrets.TWILIO_ACCOUNT_SID,
    secrets.TWILIO_AUTH_TOKEN)


class SMSUser(object):
    """Represents a user of this service."""

    def __init__(self, notify_number, relevant_text):
        """
        Args:
            notify_number: String, the phone number to send sms to ('+1XXXYYYZZZZ')
            relevant_text: String, the sub-tweet this user cares about
        """
        self.notify_number = notify_number
        self.relevant_text = relevant_text

    def handle(self, text):
        if self._cares_about(text):
            self._send(text)

    def _cares_about(self, text):
        return self.relevant_text in text

    def _send(self, text):
        try:
            TWILIO_CLIENT.messages.create(
                body=text,
                to=self.notify_number,
                from_=secrets.TWILIO_PHONE_NUMBER)
        except TwilioRestException as e:
            print e


class UserListener(tweepy.StreamListener):
    """Tweet listener that can send SMS."""

    def __init__(self, users):
        """
        Args:
            users: A list of SMSUsers
        """
        super(UserListener, self).__init__()
        self.users = users

    def on_error(self, status_code):
        # TODO: this is useless, do something smarter here
        print status_code

    def on_status(self, status):
        """Overrides base class; called when a new tweet is pushed to us."""
        for user in self.users:
            user.handle(status.text)


# Twitter user ids
UCB_NYC_USER_ID = '289051336'  # @UCBClassesNYC
ACCOUNTS_TO_LISTENERS = {
    UCB_NYC_USER_ID: SMSUser('+12067187746', 'Improv 201'),  # Sean
    UCB_NYC_USER_ID: SMSUser('+12068544595', 'Improv 101')   # Isaac
}


def connect_and_listen():
    auth = tweepy.OAuthHandler(secrets.TWITTER_CONSUMER_KEY, secrets.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(secrets.TWITTER_ACCESS_TOKEN, secrets.TWITTER_ACCESS_TOKEN_SECRET)
    twitter_api = tweepy.API(auth)

    users = ACCOUNTS_TO_LISTENERS.values()
    account_ids_to_follow = list(set(ACCOUNTS_TO_LISTENERS.keys()))

    listener = UserListener(users)
    stream = tweepy.Stream(
        auth=twitter_api.auth,
        listener=listener)

    # Wait for tweets and act on them. This call is syncronous and blocks.
    stream.filter(follow=account_ids_to_follow)


if __name__ == '__main__':
    connect_and_listen()

