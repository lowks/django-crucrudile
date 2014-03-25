"""
#TODO: Add module docstring
"""
from django.test import TestCase
from django.db.models import Model

from django_pstch_helpers.models import UserNamed, UserDescribed

class UserNamedModelTestCase(TestCase):
    class UserNamedTestModel(UserNamed, Model):
        pass

    def setUp(self):
        self.model = self.UserNamedTestModel
        self.instance = self.model(name="test_name")

    def test_unicode(self):
        self.assertEqual(
            str(self.instance),
            "test_name"
        )

class UserDescribedModelTestCase(TestCase):
    class UserDescribedTestModel(UserDescribed, Model):
        pass

    def setUp(self):
        self.model = UserDescribedTestModel
        #TODO: this
