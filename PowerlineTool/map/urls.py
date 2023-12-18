from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('log_hello/', views.log_hello, name='log_hello'),  # New URL pattern
    path('log_coordinates/', views.log_coordinates, name='log_coordinates'),
    path('addFeature/', views.addFeature, name='addFeature'),
    path('getFeature/', views.getFeature, name='getFeature'),
    path('remFeature/', views.remFeature, name='remFeature'),
    path('validateStepOne/', views.validateStepOne, name='validateStepOne')
]
