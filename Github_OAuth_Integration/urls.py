from django.contrib import admin
from django.urls import path, include
from .views import *



urlpatterns = [
    path('todo-list-get/', TodoListApiView.as_view()),
    path('check-authenticated-user/', CheckAuthenticatedUser.as_view()),
    path('login_github_user_token/', OAuthLoginGithubUser.as_view()),
    path('github/', GitHubLogin.as_view(), name='github_login')

]