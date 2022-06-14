from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.login, name='login'),
    path('bad_login/', views.login, name='bad_login'),

    path('logout/', views.logout, name='logout'),

    path('signup/', views.signup, name='signup'),

    path('profile/', views.profile, name='profile'),

]