
from django.urls import path
from .views import home_view, sendData, upload_file

urlpatterns = [
    
    path('',home_view),
    path('sendData', sendData, name="sendData"),
    path('upload', upload_file, name="upload"),
]
