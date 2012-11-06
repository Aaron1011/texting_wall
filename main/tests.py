"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from main.views import _split_message
from main.models import Wall
from django.contrib.auth.models import User
class SMSTest(TestCase):

    def test_sms_keyword(self):
        user = User.objects.create_user('Bob', 'Bob')
        user.save()


        a = Wall()
        a.hashtag = "#abc"
        a.sms_keyword = 'abc'
        a.user = user
        a.save()

        self.assertEquals(_split_message('abc Hello world'), ('abc', 'Hello world'))
        self.assertEquals(_split_message('Hello abc world'), ('abc', 'Hello world'))
        self.assertEquals(_split_message('Hello world abc'), ('abc', 'Hello world'))

        a.sms_keyword = 'AbC'
        a.save()

        self.assertEquals(_split_message('Hello AbC world'), ('AbC', 'Hello world'))

        a.sms_keyword = 'abC'
        a.save()

        self.assertEquals(_split_message('Hello world abC'), ('abC', 'Hello world'))
