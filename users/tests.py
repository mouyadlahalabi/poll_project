
        
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class DecoratorTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        
        self.admin_user = self.User.objects.create_user(
            username='admin_user', password='admin123', role='admin'
        )
        
    
        self.customer_user = self.User.objects.create_user(
            username='customer_user', password='customer123', role='customer'
        )
        
        self.no_role_user = self.User.objects.create_user(
            username='no_role_user', password='norole123'
        )
    
    def test_admin_required_success(self):
        self.client.login(username='admin_user', password='admin123')
        response = self.client.get(reverse('users:admin_dashboard'))
        self.assertEqual(response.status_code, 200)  

    def test_admin_required_failure(self):
        self.client.login(username='customer_user', password='customer123')
        response = self.client.get(reverse('users:admin_dashboard'))
        self.assertRedirects(response, reverse('users:error_403'))  

    def test_user_required_success(self):
        self.client.login(username='customer_user', password='customer123')
        response = self.client.get(reverse('users:user_dashboard'))
        self.assertEqual(response.status_code, 200)  

    def test_user_required_failure(self):
        self.client.login(username='admin_user', password='admin123')
        response = self.client.get(reverse('users:user_dashboard'))
        self.assertRedirects(response, reverse('users:error_403'))  

    def test_redirect_unauthenticated(self):
        response = self.client.get(reverse('users:admin_dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next=/users/admin_dashboard/")