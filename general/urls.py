from constituent_operations.views import GetUserInfoView
from django.urls import path
from .views import *
from superadmin_operations.views import RetrieveActionPlanSwitchStatus, RetrieveAssessmentSwitchStatus, RetrieveForumSwitchStatus, RetrieveShowNoticeStatus, RetrieveShowAssNoticeStatus
# from .consumer import LiveMessenger


urlpatterns = [
    path("send-message/", SendMessageMPView.as_view(), name="send_message"),
    path("get-user-info/<id>/", GetUserInfoView.as_view(), name="user_info"),
    path("get-actionplan-status/", RetrieveActionPlanSwitchStatus.as_view(), name="actionplan_status"),
    path("get-assessment-status/", RetrieveAssessmentSwitchStatus.as_view(), name="assessment_status"),
    path("get-notice-status/", RetrieveShowNoticeStatus.as_view(), name="show_notice"),
    path("get-as-notice-status/", RetrieveShowAssNoticeStatus.as_view(), name="show_notice"),
    path("get-forum-status/", RetrieveForumSwitchStatus.as_view(), name="forum_status"),
    path("edit-profile/<id>/", EditProfileView.as_view(), name="edit_profile"),
    


    # For Emma
    path("all-countries/", ListCountriesView.as_view(), name="emma_countries"),
    path("all-regions/<id>/", ListRegionView.as_view(), name="emma_regions"),
    path("all-constituencies/<id>/", ListConstituencyView.as_view(), name="emma_const"),
    path("all-towns/<id>/", ListTownView.as_view(), name="emma_towns"),
    path("all-areas/<id>/", ListAreaView.as_view(), name="emma_area"),

    path("unread-info/<id>/", UnreadsView.as_view(), name="unreads"),
    path("set-unread-messages-to-read/<receiver>/<sender>/", ReadMessagesView.as_view(), name="read_messages"),

    # Forum URLS
    path("send-message-to-forum/", SendMessageToForum.as_view(), name="forummessage"),
    path("retrieve-forum-messages/<id>/", RetrieveForumMessages.as_view(), name="getforummessage"),


    path("check-for-mp/<id>/", CheckIfMpIsAvailable.as_view(), name="mpis")

]
