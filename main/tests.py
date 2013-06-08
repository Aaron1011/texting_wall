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
from main.management.commands._listen_for_tweets import TwitterListener 
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
        print "Single wall"
        self.assertEquals(_split_message('This is a sentence', ''), (self.wall.hashtag, 'This is a sentence'))
        print "Done"

    def test_phone_number(self):
        print "Phone number"
        self.wall2.save()

        self.assertEquals(_split_message('Test message', '+12223334444'), (None, None))

        self.assertEquals(_split_message('Hello world',
            self.wall.phone_number), (self.wall.hashtag, 'Hello world'))
        self.assertEquals(_split_message('Hello world',
            self.wall.phone_number), (self.wall.hashtag, 'Hello world'))
        self.assertEquals(_split_message('Hello world', '+12223334444'), (None, None))
        print "Done"

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
        print "Starting browser"
        self.browser = webdriver.Firefox()
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,
                settings.TWITTER_ACCESS_TOKEN_SECRET)
        self.twitter = tweepy.API(auth)

        self.twitter_listener = TwitterListener()

    def tearDown(self):
        self.browser.close()
        self.twitter_listener.exit()

    def test_send_tweet(self):
        print "Browser test"
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

        twitter_hashtag = "#" + str(random.random())
        message = "%s %s" % (twitter_hashtag, random.random())

        hashtag = self.browser.find_element_by_id("inputHashtag")
        hashtag.send_keys(twitter_hashtag)
        hashtag.submit()
        self.twitter_listener.update()

        print message
        self.twitter.update_status(message)
        time.sleep(.5)
        self.browser.find_element_by_xpath("//p[contains(text(), '%s')]" %
                message)
        print "Done"
