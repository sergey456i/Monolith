
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('question/create/', views.create_question, name='create_question'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
]