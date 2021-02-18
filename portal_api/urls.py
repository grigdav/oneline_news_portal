from django.urls import path
from django.conf.urls import url, handler404
from .views import * 

urlpatterns = [
    path('', NewsListView.as_view(), name='home-page'),
    path('category/<str:category>/', CategoryNewsListView.as_view(), name='news_filter'),
    path('news/<str:title>/', news_detail, name='news_detail'), 
]
handler404 = 'portal_api.views.custom_404'
