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






class PubnubListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        message = json.loads(data)
        tweet = re.match("(\S*)\s(.*)", str(message['text']))
        print tweet.group(1)
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



def main():
    pubnub = Pubnub.Pubnub(settings.PUBLISH_KEY, settings.SUBSCRIBE_KEY, settings.SECRET, False)
    hashtags = set()

    auth = OAuthHandler(settings.consumer_key, settings.consumer_secret)
    auth.set_access_token(settings.access_token, settings.access_token_secret)
    print("Oauth Hander has consumer key {0} and consumer secret {1}".format(settings.consumer_key,settings.consumer_secret))
    print("Oauth handler has access token {0} and access token secret {1}".format(settings.access_token, settings.access_token_secret))
    stream = None
    while True:
        current_hashtags = set(w.hashtag for w in Wall.objects.all())
        if len(current_hashtags - hashtags) > 0:
            if stream is not None:
                stream.disconnect()
            stream = Stream(auth, PubnubListener(pubnub))
            hashtags = current_hashtags
            print("Now filtering " + ", ".join(list(hashtags)))
            stream.filter(track=[hashtags], async=True)
        time.sleep(5)

if __name__ == '__main__':
    main()
