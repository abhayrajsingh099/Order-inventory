from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('users/<int:id>/orders', views.list_user_order, name='list_user_order')
]