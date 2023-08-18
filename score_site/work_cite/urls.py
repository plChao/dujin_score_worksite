from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name="about"),
    path('student', views.student, name="student"),
    path('show_score_table/<exam_id>', views.show_score_table, name="show_score_table"),
    path('update_score_table/<exam_id>', views.update_score_table, name="update_score_table"),
    path('login', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
]
