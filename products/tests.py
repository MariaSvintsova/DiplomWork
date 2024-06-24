import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'  # Replace with your settings module path

import django
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class ProductTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test_email', password='password')
        self.product = Product.objects.create(name='Test Product', price=10.00)

    def test_product_detail_view(self):
        response = self.client.get(reverse('products:product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_product_update_view(self):
        response = self.client.get(reverse('products:product_update', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_form.html')

    def test_toggle_activity_view(self):
        response = self.client.post(reverse('products:toggle_activity', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)  # Redirects to success_url
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_active)

    def test_product_create_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('products:create_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_form.html')

        response = self.client.post(reverse('products:create_product'), {
            'name': 'New Product',
            'price': 20.00,
        })
        self.assertEqual(response.status_code, 302)


    def test_product_list_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
