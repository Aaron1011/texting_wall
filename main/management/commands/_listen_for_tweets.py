from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from django.conf import settings
from tweepy.api import API
from main.models import Wall, Message
import Pubnub
import json
import re
import time
import datetime
from django.utils.timezone import utc


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
        if 'text' in message:
            tweet = re.search("(#\S+)", str(message['text']))
            hashtag = tweet.group(1)
            print hashtag
            print self.pubnub.publish({
                'channel': hashtag,
                'message': {
                    'message': str(message['text'])
                }
            })


            wall = Wall.objects.filter(hashtag__iexact=hashtag)
            if len(wall) > 0:
                message2 = Message()
                message2.message = str(message['text'])
                message2.hashtag = hashtag
                message2.twitter_account = str(message['user']['screen_name'])
                message2.wall = wall[0]
                print "Saving message"
                message2.save()

        else:
            print message
        return True

    def on_error(self, status):
        print status


def main():
    pubnub = Pubnub.Pubnub(settings.PUBNUB_PUBLISH_KEY, settings.PUBNUB_SUBSCRIBE_KEY, settings.PUBNUB_SECRET, False)
    hashtags = set()

    auth = OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    stream = None
    print "Started"
    while True:
        try:
            #current_hashtags = set(w.hashtag for w in Wall.objects.filter(last_ping__gt=datetime.datetime.now(utc) - datetime.timedelta(minutes=settings.WALL_EXPIRATION)))
            current_hashtags = set(w.hashtag for w in Wall.objects.all())
            if len(current_hashtags - hashtags) > 0:
                if stream is not None:
                    stream.disconnect()
                stream = Stream(auth, PubnubListener(pubnub))
                hashtags = current_hashtags
                print("Now filtering " + ", ".join(list(hashtags)))
                stream.filter(track=list(hashtags), async=True)
            time.sleep(5)
        except KeyboardInterrupt:
            stream.disconnect()
            quit()
        except Exception as e:
            print e
        time.sleep(5)

if __name__ == '__main__':
    main()
