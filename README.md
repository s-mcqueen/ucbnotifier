# ucbnotifier

Sends SMS when UCB Improv classes in NYC open up. Easily changable to listen to any
stream of tweets, apply an arbitrary text filter and send sms notifications.

Setup:
* Create a "secrets.py" file following the example in "secrets_example.py" -- you'll need to setup Twitter dev and Twilio accounts if you haven't...
* pip install -r requirements.txt # do this in a venv
* python notifier.py # this blocks and will keep running
* go run this on a server somewhere!

Note to self: I have gcloud, kubectl, docker, virtualenv installed which are all required for how I'm running and deploying this
