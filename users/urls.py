from django.urls import path
from . import views

urlpatterns = [
    path("create-constituent-account/", views.ConstituentCreateApiView.as_view(), name="createconstituent"),
    path("create-mp-account/", views.MPCreateApiView.as_view(), name="createmp"),
    path("create-secondary-account/<user_id>", views.SecondaryRegistration.as_view(), name="secondary_create"),

]
