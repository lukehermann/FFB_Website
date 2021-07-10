from django.urls import path
from FFB_Website import views

urlpatterns = [
    path("", views.home, name="home"),
]