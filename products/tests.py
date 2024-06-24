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

    # def test_product_detail_view(self):
    #     # Аутентифицируем пользователя
    #     self.client.force_login(self.user)
    #
    #     # Проверяем доступ к странице деталей продукта
    #     response = self.client.get(reverse('products:product_detail', args=[self.product.pk]))
    #
    #     # Проверяем успешность запроса
    #     self.assertEqual(response.status_code, 200)
    #
    #     # Проверяем использование правильного шаблона
    #     self.assertTemplateUsed(response, 'products/product_detail.html')
    # def test_product_update_view(self):
    #     response = self.client.get(reverse('products:product_update', args=[self.product.pk]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'products/product_form.html')

    def test_toggle_activity_view(self):
        response = self.client.post(reverse('products:toggle_activity', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)  # Redirects to success_url
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_active)

    # def test_product_create_view(self):
    #     # Проверяем GET запрос на страницу создания продукта
    #     response = self.client.get(reverse('products:create_product'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'products/product_form.html')
    #
    #     # Проверяем POST запрос на создание нового продукта
    #     response = self.client.post(reverse('products:create_product'), {
    #         'name': 'New Product',
    #         'price': 20.00,
    #     })
    #
    #     # Ожидаем перенаправление на success_url с кодом 302
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('products:home'))

    def test_product_list_view_authenticated(self):
        # Логинимся как созданный пользователь
        self.client.login(username='testuser', password='password')

        # Используем правильное имя URL для списка продуктов (products:home)
        response = self.client.get(reverse('products:home'))

        # Проверяем, что произошло перенаправление
        self.assertEqual(response.status_code, 302)

        # Проверяем адрес перенаправления
        self.assertRedirects(response, reverse('users:login') + '?next=' + reverse('products:home'))
