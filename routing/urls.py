from django.urls import path
from .views import *


urlpatterns = [
    path('pageviews/<id>/', WebPageView.as_view(), name="pages"),
    path('sidebar/<id>/', SideBarView.as_view(), name="sidebar"),

]
