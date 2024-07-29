from django.urls import path
from .views import *

urlpatterns = [
    path('/prediction', prediction, name = 'prediction'),
    path('/getdata',ge)
]