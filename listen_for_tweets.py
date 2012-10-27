from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from django.core.management import setup_environ
from texting_wall import settings
setup_environ(settings)

from main.models import Wall
from main import Pubnub
import json, re
import time
from django.conf import settings as app_settings
pubnub = Pubnub.Pubnub(app_settings.PUBLISH_KEY, app_settings.SUBSCRIBE_KEY, app_settings.SECRET, False)
hashtags = []




class PubnubListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        message = json.loads(data)
        if message.has_key('text'):
            tweet = re.match("(\S*)\s(.*)", str(message['text']))
            wall = Wall.objects.filter(hashtag__exact=tweet.group(1))
            pubnub.publish({
            'channel' : wall[0].sms_keyword,
            'message' : {
                'message' : tweet.group(2)
                }
            })
        else:
            print message
        return True

    def on_error(self, status):
        print status

l = PubnubListener()
auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

def main():
    while True:
        all_walls = Wall.objects.all()
        for wall in all_walls:
            if not wall.hashtag in hashtags:
                print wall.hashtag
                hashtags.append(wall.hashtag)
                stream = Stream(auth, l)
                stream.filter(track=[wall.hashtag], async=True)
                time.sleep(5)

if __name__ == '__main__':
    main()
