from django.urls import path
from .views import  *

urlpatterns = [
    path("message/", SendMessageViaMicroServiceView.as_view(), name="send_message_via_microservices")
]