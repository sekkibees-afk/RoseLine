from django.urls import path
from . import views

app_name = 'roseline'

urlpatterns = [
    path('', views.index, name='index'),
    path('horses/', views.horses, name='horses'),
    path('account/', views.account, name='account'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path("horses/add/", views.add_horse, name="add_horse"),
    path('horses/<slug:slug>/', views.horse_detail, name='horse_detail'),
    path("logout/", views.log_out, name="logout")
]