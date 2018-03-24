from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'remove_favorite$', views.remove_favorite),
    url(r'add_favorite$', views.add_favorite),
    url(r'create_quote$', views.create_quote),
    url(r'$', views.index),
]