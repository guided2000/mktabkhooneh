from django.urls import path
from blog.views import *

app_name ='blog'

urlpatterns = [
    path('',blog_views,name='index'),
    path('<int:pid>' ,blog_single,name='single'),
    path('category/<str:cat_name>',blog_views,name='category'),
    path('tag/<str:tag_name>',blog_views,name='tag'),
    path('author/<str:author_username>',blog_views,name='author'),
    path('search/',blog_search,name='search'),
    path('newsletter/',newsletter_view,name='newsletter'), 

]