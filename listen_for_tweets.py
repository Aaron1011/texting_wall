from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from main.models import Wall

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=""
consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=""
access_token_secret=""

auth = OAuthHandler(consumer_key, consumer_secret).set_access_token(access_token, access_token_secret)
def main():
    walls = []
    while True:
        objects = Wall.objects.all()
        for item in objects:
            if not item.hashtag in walls:
                walls.append(item.hashtag)
                stream = Stream(auth, StdOutListener())
                stream.filter(track=[item.hashtag])

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
	This is a basic listener that just prints received tweets to stdout.

	"""
    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    main()
