from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='sign_up'),   # Signup path
    path('users/', views.user_list, name='user_list'), # a webpage to view registered users
]