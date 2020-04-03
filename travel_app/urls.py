from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('travelPlan', views.travelPlan),
    path('addPlan', views.addPlan),
    path('join/<tripID>', views.join),
    path('destination/<tripID>', views.destination)
]