from django.urls import path
from . import views

app_name = 'trends'
urlpatterns = [
    path('keyword/', views.keyword, name='keyword'),
    path('keyword/<int:pk>/', views.delete, name='delete'),
    path('crawling/', views.crawling, name='crawling'),
    path('crawling/histogram/', views.histogram, name='crawling_histogram'),
    path('crawling/advanced/', views.acvanced, name='crawling_advanced'),
]
