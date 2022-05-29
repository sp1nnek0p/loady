from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('createload/', views.create_load_view, name='createload'),
    path('loadview/<str:id>/', views.load_view, name='loadview'),
    path('editload/<str:id>/', views.edit_load_view, name='editload'),
    path('profile/<str:id>/', views.profile_view, name='profile'),
    path('delete/<str:id>/', views.delete_room_view, name="delete"),
    path('editprofile/<str:id>/', views.edit_profile_view, name='editprofile'),
    path('messages/<str:id>/', views.messages_view, name='messages'),
    path('message/<str:id>/', views.message_view, name='message'),
    path('sendmessage/<str:id>/', views.send_message_view, name='sendmessage'),
]
