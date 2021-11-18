from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin', admin.site.urls),
    path('',views.hello_world, name='hellowolds' ),
    path('get', views.example_view, name='hellowolds'),
    path('login', obtain_auth_token),
    path('register', views.register, name='register'),

]