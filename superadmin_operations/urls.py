from django.urls import path
from . import views

urlpatterns = [
    path("switch-action-plan/<id>/", views.SwitchActionPlanOnOrOffView.as_view(), name="switch-actionplan"),
    

]
