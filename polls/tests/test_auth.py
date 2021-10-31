"""Tests of authentication."""
import django.test
from django.urls import reverse
from django.contrib.auth.models import User


class UserAuthTest(django.test.TestCase):

    def setUp(self):
        super().setUp()
        self.username = "testuser"
        self.password = "Fat-Chance!"
        self.user1 = User.objects.create_user(
                        username=self.username,
                        password=self.password,
                        email="testuser@nowhere.com")
        self.user1.first_name = "Tester"
        self.user1.save()
    
    def test_login_view(self):
        """Test that a user can login via the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        # Can login using POST
        # usage: client.post(url, {'key1":"value", "key2":"value"})
        form_data = {"username": "testuser", "password": "Fat-Chance!"}
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse("polls:index"))
    
    # def test_auth_require_to_vote(self):
    #     """Test that authentication is require to submit a vote."""
    #     login_url = reverse("login")
    #     # Can get the login page
    #     response = self.client.get(login_url)
    #     self.assertEqual(200, response.status_code)
    #     # Can login using POST
    #     # usage: client.post(url, {'key1":"value", "key2":"value"})
    #     form_data = {"username": "testuser", "password": "Fat-Chance!"}
    #     response = self.client.post(login_url, form_data)
    #     self.assertEqual(302, response.status_code)
    #     # should redirect us to the polls index page ("polls:index")
    #     self.assertRedirects(response, reverse("polls:index"))