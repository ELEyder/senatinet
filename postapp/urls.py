from django.urls import path
from .views import *

urlpatterns = [
    path('like/<str:id_post>/', like, name='like'),
    path('postear/', postear, name='postear'),
]