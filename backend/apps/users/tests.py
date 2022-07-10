import factory
import json
import random

from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.test.factory import *
from users.models import *
from users.views import *
from faker import Faker
from django.contrib.auth.models import Group
from rest_framework.test import APIRequestFactory, force_authenticate

from users import views, util

from rest_framework.renderers import JSONRenderer

from backend.settings.common import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_URL

import boto3


def convert_to_dict_from(model):
    data = { key: value if type(value) is str or type(value) is int else str(value)
        for key, value in model.__dict__.items() if key is not '_state' and value is not None }
    return data


def createTestData():
    util.prepare()
    User.objects.create_superuser("tomoya", "tomoya@example.com", "youluck123")
    User.objects.create_guest_user("guest")
    User.objects.create_unique_user("general@example.com", username="general")
    User.objects.create_researcher("researcher", "researcher@example.com", "password")
    

class EmailUserAPITestCase(APITestCase):
    def setUp(self):
        createTestData()
    
    def test_get_emailuser(self):
        user = EmailUserFactory.create(password="password")
        self.assertTrue(self.client.login(username="tomoya", password="youluck123"))
        response = self.client.get(f"/api/users/{user.id}/")
        self.assertTrue(response.status_code == 200)


class DownloadEmailListAPITestCase(APITestCase):
    def setUp(self):
        createTestData()

    def test_is_accessible_to_get_download_curve_data(self):
        request = RequestFactory.create(participants=[EmailUserFactory.create() for _ in range(10)])
        for _ in range(5):
            CurveFactory.create(room_name=request.room_name)
        response = self.client.get(f"/api/get_download_curve_data/{request.id}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue("url" in response.json())
    
    def test_is_inaccessible_to_get_download_curve_data(self):
        response = self.client.get(f"/api/get_download_curve_data/{100}")
        self.assertTrue(response.status_code == 404)


class ResetEmailAddressesFromRequest(APITestCase):
    def setUp(self):
        createTestData()
    
    def test_is_accessible_to_reset_email_addresses_api(self):
        request = RequestFactory.create(participants=[EmailUserFactory.create() for _ in range(10)])
        response = self.client.get(f"/api/reset_email_addresses/{request.id}")
        self.assertTrue(response.status_code == 200)
