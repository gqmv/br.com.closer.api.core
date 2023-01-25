from django.test import TestCase

class TestUserRegisterEndpoint(TestCase):
    endpoint = "/api/register/"
    
    def test_register_user(self):
        pass