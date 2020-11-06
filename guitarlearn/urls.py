from django.urls import path, re_path
from . import views

app_name = 'guitarlearn'

urlpatterns = [
    # path("learn/<str:key>/", views.tutorial_detail, name="tutorial_detail"),
    path("", views.index, name="index"),
    path("video_detail/<str:key>", views.video_detail, name="video_detail"),
    path("playlist/<str:username>", views.playlist, name="playlist"),
    path('search_list/',views.search_list, name="search_list"),
    path('video_detail/<str:key>/like/', views.video_like, name='video_like'),
    path('video_detail/<str:key>/unlike/', views.video_unlike, name='video_unlike'),
    path('video/search', views.video_search, name='video_search'),
    re_path(r'^(?P<username>[\w.@+-]+)/$', views.user_page, name='user_page'),
]
