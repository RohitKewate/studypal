from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage,name= "login-page"),
    path('register/', views.registerPage,name= "register-page"),
    path('logout/', views.logoutPage,name= "logout-page"),
    path('', views.home, name="home-page"),
    path('room/<str:pk>/', views.room, name="room-page"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile-page"),
    path('create-room/', views.createRoom, name="create-room-page"),
    path('update-room/<str:pk>',views.updateRoom, name="update-room-page"),
    path('delete-room/<str:pk>',views.deleteRoom, name="delete-room-page"),
    path('delete-message/<str:pk>',views.deleteMessage, name="delete-message-page"),
    path('update-user/', views.updateUser, name="update-user-page"),
    path('topics/', views.topicsPage, name="topics-page"),
    path('activity', views.activityPage, name="activity-page")
]

