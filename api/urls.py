from django.urls import path, include
from rest_auth.views import LoginView, LogoutView

urlpatterns = [
    path('login', LoginView.as_view(), name="user-login"),
    path('logout', LogoutView.as_view(), name='user-logout'),
    path(
        'register',
        include('rest_auth.registration.urls'),
        name="user-auth-registration"
    ),
]
