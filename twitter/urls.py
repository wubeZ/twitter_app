from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('explore/', views.explore, name="explore"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('tweet_like/<int:pk>', views.tweet_like, name="tweet_like"),
    path('tweet_update/<int:pk>', views.update_tweet, name ="tweet_update"),
    path('tweet_delete/<int:pk>', views.delete_tweet, name ="tweet_delete")
]
