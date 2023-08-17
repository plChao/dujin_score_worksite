from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name="about"),
    path('login', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
]