from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note

# Create your tests here.
class NotesViewsTests(TestCase):
    
    def test_signup(self):
        username = 'username'
        email = 'email@example.com'
        password = 'password'
        response = self.client.post(reverse("notes:signup"), data={'username': username, 'email': email, 'password': password})
        self.assertRedirects(response, reverse("notes:all"))
        self.assertEqual(response.status_code, 302)
        self.client.login(username=username, password=password)
        user = User.objects.get(username=username)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, email)
    
    def test_failed_signin(self):
        self.test_signup()
        response=self.client.post(reverse("notes:signin"),data={'username':'wronguser','password':'wrongpassword'})
        self.assertEqual(response.status_code, 404)
        
    def test_successful_signin(self):
        self.test_signup()
        response=self.client.post(reverse("notes:signin"),data={'username':'username','password':'password'})
        self.assertRedirects(response, reverse("notes:all"))
        self.assertEqual(response.status_code, 302)
        
    def test_addnote(self):
        self.test_successful_signin()
        response = self.client.post(reverse("notes:add"), data={'content': 'content', 'expiration': '2024-10-10T01:01', 'views_limit': 10})
        self.assertRedirects(response, reverse("notes:all"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.count(), 1)
        n = Note.objects.get(content="content")
        self.assertIsNotNone(n)
        self.assertEqual(n.views_limit, 10)
        print(n.expiration)
        
    def test_allnotes(self):
        self.test_successful_signin()
        response=self.client.get(reverse("notes:all"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['notes'], [])
       
        