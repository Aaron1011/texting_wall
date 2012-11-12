from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from django.core.management import setup_environ
from texting_wall import settings
setup_environ(settings)
from tweepy.api import API
from main.models import Wall, Message
from main import Pubnub
import json, re
import time
import sys, signal


class PubnubListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """
    def __init__(self, pubnub, api=None):
        self.api = api or API()
        self.pubnub = pubnub

    def on_data(self, data):
        message = json.loads(data)
        print message
        if message.has_key('text'):
            tweet = re.search("(#\S+)", str(message['text']))
            print tweet.group(1)
            wall = Wall.objects.filter(hashtag__iexact=tweet.group(1))
            if len(wall) > 0:
                message2 = Message()
                message2.message = str(message['text'])
                message2.hashtag = wall[0].hashtag
                message2.twitter_account = str(message['user']['screen_name'])
                message2.wall = wall[0]
                message2.save()

                self.pubnub.publish({
                    'channel' : wall[0].hashtag,
                    'message' : {
                        'message' : str(message['text'])
                    }
                })
        else:
            print message

        return True            

    def on_error(self, status):
        print status


def main():
    pubnub = Pubnub.Pubnub(settings.PUBLISH_KEY, settings.SUBSCRIBE_KEY, settings.SECRET, False)
    hashtags = set()

    auth = OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    stream = None
    while True:
        try:
            current_hashtags = set(w.hashtag for w in Wall.objects.all())
            if len(current_hashtags - hashtags) > 0:
                if stream is not None:
                    stream.disconnect()
                stream = Stream(auth, PubnubListener(pubnub))
                hashtags = current_hashtags
                print("Now filtering " + ", ".join(list(hashtags)))
                stream.filter(track=list(hashtags), async=True)
            time.sleep(5)
        except Exception as e:
            print e

if __name__ == '__main__':
    main()
