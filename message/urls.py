from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/[\d+].*?', views.messages)
]
