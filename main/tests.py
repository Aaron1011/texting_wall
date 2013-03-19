"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, LiveServerTestCase
from main.views import _split_message
from main.models import Wall
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core import management
from os import environ
from selenium import webdriver
import random
import tweepy
import time

class SMSTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('Bob', None, 'Bob')
        self.user.save()
        self.wall = Wall(hashtag="#abc", phone_number="+11112223333",
                user=self.user)
        self.wall2 = Wall(hashtag="#qwe", phone_number="+11234567891",
                user=self.user)

        self.wall.save()

    def test_single_wall(self):
        self.assertEquals(_split_message('This is a sentence', ''), (self.wall.hashtag, 'This is a sentence'))

    def test_phone_number(self):
        self.wall2.save()

        self.assertEquals(_split_message('Test message', '+12223334444'), (None, None))

        self.assertEquals(_split_message('Hello world',
            self.wall.phone_number), (self.wall.hashtag, 'Hello world'))
        self.assertEquals(_split_message('Hello world',
            self.wall.phone_number), (self.wall.hashtag, 'Hello world'))
        self.assertEquals(_split_message('Hello world', '+12223334444'), (None, None))

    #def test_purchase_phone_number(self):

class WallTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Bob', None, 'Bob')
        self.user.save()
        self.wall = Wall(hashtag="#abc", phone_number="+11112223333",
                user=self.user)
        self.wall.save()

    #def test_display_wall(self):

class AcceptanceTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,
                settings.TWITTER_ACCESS_TOKEN_SECRET)
        self.twitter = tweepy.API(auth)
        management.call_command('listen_for_tweets')

    def tearDown(self):
        self.browser.close()

    def test_send_tweet(self):
        self.browser.get(self.live_server_url + reverse('main.views.index'))
        self.assertEqual(self.browser.title, "Texting Wall")
        self.browser.get(self.live_server_url + reverse('main.views.create_account'))
        self.assertEqual(self.browser.title, "Create account")
        self.browser.find_element_by_id("id_username").send_keys("test")
        self.browser.find_element_by_id("id_password1").send_keys("test")
        self.browser.find_element_by_id("id_password2").send_keys("test")
        self.browser.find_element_by_id("id_password2").submit()
        self.assertEqual(self.browser.current_url, self.live_server_url +
                reverse('main.views.index'))

        self.browser.get(self.live_server_url + reverse('main.views.new_wall'))
        hashtag = self.browser.find_element_by_id("inputHashtag")
        hashtag.send_keys("#walltest")
        hashtag.submit()

        message = "#%s %s" % (random.random(), random.random())
        print message
        self.twitter.update_status(message)
        time.sleep(.5)
        self.browser.find_element_by_xpath("//p[contains(text(), '%s')]" %
                message)

