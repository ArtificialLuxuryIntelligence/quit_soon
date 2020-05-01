from django.urls import path
from django.contrib.auth import views as auth_views

from . import views # import views so we can use them in urls.

app_name = 'QuitSoonApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    # path('login/', view.login, name='Login'),
]
