from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addFeature/', views.addFeature, name='addFeature'),
    path('getFeature/', views.getFeature, name='getFeature'),
    path('remFeature/', views.remFeature, name='remFeature'),
    path('validation/', views.validation, name='validation'),
    path('fuse/', views.fuse, name='fuse'),
    path('divide/', views.divide,name='divide'),
    path('export/', views.export, name='export')
]
