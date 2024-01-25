from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.user_login_page, name="login_page"),
    path("signup/", views.user_signup_page, name="signup_page"),
    path("logout/", views.user_logout, name="logout"),
]
