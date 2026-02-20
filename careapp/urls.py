from django.contrib import admin
from django.urls import path
from careapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.home, name='home' ),
    path('starter/', views.starter, name='starter' ),


]
