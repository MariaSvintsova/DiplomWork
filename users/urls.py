from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView
from django.urls import path
from users.views import RegisterView, registration_success, ProfileView, PasswordResetView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register_success/', registration_success, name='register_success'),
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='products:home'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
]
