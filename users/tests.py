# from django.test import TestCase, Client
# from django.urls import reverse
# from django.core import mail
# from users.models import User
# from users.forms import UserRegisterForm  # убедитесь, что импорт формы корректный
#
# class UserTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')
#
#     def test_register_view(self):
#         response = self.client.get(reverse('users:register'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users/register.html')
#
#         response = self.client.post(reverse('users:register'), {
#             'username': 'newuser',
#             'email': 'newuser@example.com',
#             'password1': 'Password123!',
#             'password2': 'Password123!',
#         })
#         self.assertEqual(response.status_code, 302)  # Redirects to success_url
#         self.assertTrue(User.objects.filter(username='newuser').exists())
#
#     def test_login_view(self):
#         response = self.client.get(reverse('users:login'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users/login.html')
#
#         response = self.client.post(reverse('users:login'), {
#             'username': 'testuser',
#             'password': 'password',
#         })
#         self.assertEqual(response.status_code, 302)  # Redirects after login
#
#     def test_profile_view(self):
#         self.client.login(username='testuser', password='password')
#         response = self.client.get(reverse('users:profile'))
#         self.assertEqual(response.status_code, 200)
#
#         response = self.client.post(reverse('users:profile'), {
#             'username': 'updateduser',
#             'email': 'updateduser@example.com',
#         })
#         self.assertEqual(response.status_code, 302)  # Redirects after update
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.username, 'updateduser')
#
#     def test_password_reset_view(self):
#         response = self.client.get(reverse('users:password_reset'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users/password_reset.html')
#
#         response = self.client.post(reverse('users:password_reset'), {
#             'email': 'testuser@example.com',
#         })
#         self.assertEqual(response.status_code, 302)  # Redirects after password reset request
#         self.assertEqual(len(mail.outbox), 1)  # Check that one message has been sent
#
#     def test_logout_view(self):
#         self.client.login(username='testuser', password='password')
#         response = self.client.post(reverse('users:logout'))
#         self.assertEqual(response.status_code, 302)  # Redirects to login
