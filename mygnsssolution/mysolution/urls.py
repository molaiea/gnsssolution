
from django.urls import path
from .views import home_view, sendData

urlpatterns = [
    
    path('',home_view),
    path('sendData', sendData, name="sendData"),
]
