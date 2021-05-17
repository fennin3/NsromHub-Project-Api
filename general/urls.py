from constituent_operations.views import GetUserInfoView
from django.urls import path
from .views import *
from superadmin_operations.views import RetrieveActionPlanSwitchStatus
# from .consumer import LiveMessenger


urlpatterns = [
    path("send-message/", SendMessageMPView.as_view(), name="send_message"),
    path("get-user-info/<id>/", GetUserInfoView.as_view(), name="user_info"),
    path("get-actionplan-status/", RetrieveActionPlanSwitchStatus.as_view(), name="actionplan_status"),
    path("edit-profile/<id>/", EditProfileView.as_view(), name="edit_profile"),
    


    # For Emma
    path("all-countries/", ListCountriesView.as_view(), name="emma_countries"),
    path("all-regions/<id>/", ListRegionView.as_view(), name="emma_regions"),
    path("all-constituencies/<id>/", ListConstituencyView.as_view(), name="emma_const"),
    path("all-towns/<id>/", ListTownView.as_view(), name="emma_towns"),
    path("all-areas/<id>/", ListAreaView.as_view(), name="emma_area"),

]
