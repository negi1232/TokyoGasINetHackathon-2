from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('regist', views.regist, name='regist')
]