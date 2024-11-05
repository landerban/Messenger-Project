from django.urls import path
from . import views

urlpatterns = [
    path('messages/<int:recipient_id>/', views.get_messages, name='get_messages'),
    path('register/', views.register, name='register'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('chat/<str:room_name>/', views.chat_room, name = 'chat_room')
]