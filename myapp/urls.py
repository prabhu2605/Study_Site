from django.urls import path

from myapp.views import (Home, room, createroom, updateroom, deleteroom, Loginpage,
                         logout_user, Registerpage, deletemessage, userprofile, Update_user, topic_page)


urlpatterns = [
    path('', Home, name='home'),
    path('room/<str:pk>/', room, name='room'),
    path('createroom/', createroom, name='create_room'),
    path('profile/<str:pk>/', userprofile, name='profile'),
    path('updateroom/<str:pk>/', updateroom, name='update_room'),
    path('deleteroom/<str:pk>/', deleteroom, name='delete_room'),
    path('loginpage/', Loginpage, name='loginpage'),
    path('logout/', logout_user, name='logout'),
    path('register/', Registerpage, name='register'),
    path('deletemessage/<str:pk>/', deletemessage, name='delete_message'),
    path('update_user/', Update_user, name='update_user'),
    path('topic_page/', topic_page, name='topic_page')
]