from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import Staff  # or Doctor, depending on the login scenario

class LoginViewTest(TestCase):

    def test_staff_login_success(self):

        response = self.client.post(self.login_url, {
            'email': 'prasee@gmail.com',
            'password': '1234'
        })
        print('Response status code:', response.status_code)
        print('Response content:', response.content.decode())  
        print('Session:', self.client.session.items())  

        self.assertEqual(response.status_code, 302)  

        session = self.client.session
        self.assertIn('staff_id', session, "Staff ID not found in session")
        self.assertEqual(session['staff_id'], self.staff.id)