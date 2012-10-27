from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from django.core.management import setup_environ
from texting_wall import settings
setup_environ(settings)

from main.models import Wall
from main import Pubnub
import json, re

PUBLISH_KEY = "pub-8a8223f4-631c-4484-a118-2b01232307cc"
SUBSCRIBE_KEY = "sub-e754ed6b-133d-11e2-91f2-b58e6c804094"
SECRET = "sec-ZjcxZGVjNDAtZWQyMC00MGZmLTg1Y2MtNmJkNGE3YTJiYjlj"
pubnub = Pubnub.Pubnub(PUBLISH_KEY, SUBSCRIBE_KEY, SECRET, False)
hashtags = []
monitored = []

# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret will be generated for you after
consumer_key="3yyqRg7yqmyIZvzOzJI20w"
consumer_secret="lPGDVv8dSctExxkXOAqXUnQKEJPBiUJq791XC8PGeI"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="879862038-DAGmivCACAap96mZxPi4YfIRwM3Zv3TnG4SGyQYN"
access_token_secret="Olwot3CAYkPUfIVOf2pdAk2LDmN9gsd255B0Xagtjo"




class PubnubListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        message = json.loads(data)
        tweet = re.match("(\S*)\s(.*)", str(message['text']))
        wall = Wall.objects.filter(hashtag__exact=tweet.group(1))
        pubnub.publish({
            'channel' : wall[0].sms_keyword,
            'message' : {
                'message' : tweet.group(2)
            }
        })
        return True

    def on_error(self, status):
        print status

l = PubnubListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

def main():
    while True:
        all_walls = Wall.objects.all()
        for wall in all_walls:
            if not wall.hashtag in hashtags:
                print wall.hashtag
                hashtags.append(wall.hashtag)
                stream = Stream(auth, l)
                stream.filter(track=[wall.hashtag], async=True)

if __name__ == '__main__':
    main()
