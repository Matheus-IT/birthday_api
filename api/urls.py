from api import views
from django.urls import path


urlpatterns = [
    path('', views.hello_view, name='hello_view'),
]