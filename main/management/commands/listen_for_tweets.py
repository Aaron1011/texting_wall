from django.core.management.base import BaseCommand, CommandError
import _listen_for_tweets
class Command(BaseCommand):
    def handle(self, *args, **options):
        _listen_for_tweets.main()
