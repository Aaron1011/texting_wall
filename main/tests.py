"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from main.views import _split_message
from main.models import Wall
from django.contrib.auth.models import User
from django.conf import settings
from os import environ
class SMSTest(TestCase):

    def test_single_wall(self):
        user = User.objects.create_user('Bob', 'Bob')
        user.save()


        a = Wall()
        a.hashtag = "#abc"
        a.phone_number = '+11112223333'
        a.user = user
        a.save()

        self.assertEquals(_split_message('This is a sentence', ''), (a.hashtag, 'This is a sentence'))


    def test_phone_number(self):

        user = User.objects.create_user('Bob', 'Bob')
        user.save()

        self.assertEquals(_split_message('Test message', '+12223334444'), (None, None))

        a = Wall()
        a.hashtag = "#abc"
        a.phone_number = "+11234567890"
        a.user = user
        a.save()

        b = Wall()
        b.hashtag = "#qwe"
        b.phone_number = "+11234567891"
        b.user = user
        b.save()

        self.assertEquals(_split_message('Hello world', a.phone_number), (a.hashtag, 'Hello world'))
        self.assertEquals(_split_message('Hello world', b.phone_number), (b.hashtag, 'Hello world'))
        self.assertEquals(_split_message('Hello world', '+12223334444'), (None, None))

    #def test_purchase_phone_number(self):
