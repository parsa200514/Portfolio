from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('add/', views.add_device, name='add_device'),
    path('export/<task>', views.export_devices, name='export_devices'),

]
