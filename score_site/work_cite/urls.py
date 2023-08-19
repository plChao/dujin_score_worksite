from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name="about"),
    # path('create_user', views.create_user, name="create_user"),
    path('awards', views.awards, name="awards"),
    path('student', views.student, name="student"),
    path('search_student', views.search_student, name="search_student"),
    path('show_score_table/<exam_id>', views.show_score_table, name="show_score_table"),
    path('update_score_table/<exam_id>', views.update_score_table, name="update_score_table"),
    path('login', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
]
