from django.contrib import admin
from django.urls import path
from careapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, ),
    path('starter/', views.starter, name='starter' ),
    path ('appointments/', views.appointments, name='appointments' ),
    path('about/', views.about, name='about'),
    path('show/', views.show, name='show'),



]
