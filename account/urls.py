from django.contrib.auth import views
from django.urls import path,include,re_path
from .views import *
app_name= 'account'

urlpatterns =[
    path('',postlist.as_view(),name="home"),
    path('post/create',postcreate.as_view(),name="post-create"),
    path('post/update/<int:pk>',postupdate.as_view(),name="post-update"),
    path('post/delete/<int:pk>',postDelete.as_view(),name="post-delete"),
    path('profile/',Profile.as_view(),name="profile"),
    path('register/',Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>',activate, name='activate'),
    # path('',home,name="home")
]
