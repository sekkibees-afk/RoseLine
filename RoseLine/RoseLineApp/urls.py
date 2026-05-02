from django.urls import path
from . import views

app_name = 'roseline'

urlpatterns = [
    path('', views.index, name='index'),
]