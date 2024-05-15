from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name="about"),
    path('table_exists', views.table_exists, name="table_exists"),
    # path('create_user', views.create_user, name="create_user"),
    path('get_article_content/<article_id>', views.get_article_content, name="get_article_content"),
    path('get_list/<award_id>', views.get_award_list, name="get_list"),
    path('awards', views.awards, name="awards"),
    path('student', views.student, name="student"),
    path('search_student', views.search_student, name="search_student"),
    path('show_score_table/<exam_id>', views.show_score_table, name="show_score_table"),
    path('update_score_table/<exam_id>', views.update_score_table, name="update_score_table"),
    path('login', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
]
