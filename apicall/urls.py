from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('rsstats/<str:username>/', views.process_data, name='process_data'),
]