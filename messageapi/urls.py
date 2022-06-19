from django.urls import path
from . import views
from . import auth

urlpatterns = [
    path('add_user/', views.add_user),
    path('signin/', auth.CustomAuthToken.as_view()),
    path('logout/', auth.Logout.as_view()),
    path('send_message/', views.send_message),
    path('create_group/', views.create_group),
    path('add_member/', views.add_member),
    path('delete_group/', views.delete_group),
    path('edit_user/', views.edit_user),
    path('like_message/', views.like_message),
]
