from django.urls import path
from .views import *

urlpatterns = [
    path('send-message/', SendMessageConstituentView.as_view(), name="send_message"),
    path('retrieve-projects/<id>/', RetrieveProjectsView.as_view(), name="retrieve_projects"),
    path("send-incident-report/", RNSendIncidentReportView.as_view(), name="incident_report"),
    path("send-request-form/", RNSendRequestFormView.as_view(), name="requestform"),

    path("retrieve-my-constituencies/<id>/", RetrieveAllConstituencyOfConst.as_view(), name="my_constituencies"),
    path("switch-active-constituency/<user_id>/<const>/", SetActiveConstituencyView.as_view(), name="set_active_const"),
    path("comment-on-post/", CommentOnProjectAndPostView.as_view(), name="commet_on_post"),
    path("retrieve-messages/<id>/", RetriveMessageView.as_view(), name="retrieve_message"),
    path("like-project/<id>/<post_id>/", LikeProjectView.as_view(), name="like_project"),
    path("send-action-plan/<id>/", ActionPlanView.as_view(), name="action_plan"),
    path("retrieve-action-plan-summary/<id>/<date>/", RetrieveActionPlanStatForAssemblyMan.as_view(), name="action_plan_summary"),
    path("approve-action-plan/<id>/", ApproveActionPlanView.as_view(), name="approve_action"),
    path("action-titles/", RetrieveProblemTitlesView.as_view(), name="action_title"),
    path("retrieve-years/", RetrieveYearsView.as_view(), name="years"),

    path("approval-status/<id>/<year>/", GetActionPlanApprovedStatusView.as_view(), name="status"),

    # SUBADMIN URLS
    path("create-project-for-mp/", CreateProjectForMP.as_view(), name="create_project_for_mp"),
    path("reply-message-for-mp/<id>/", ReplyNotification.as_view(), name="reply_notification"),

    # Assessment
    path("retrive-projects-for-assessment/<id>/<year>/", RetrieveProjectsForAssessmentView.as_view(), name="projects_for_assessment"),
    path("retrive-conducts-for-assessment/", RetrieveConductsForAssessmentView.as_view(), name="conducts_for_assessment"),
    path("send-assessment/<id>/", SendAssessmentView.as_view(), name="send_assessment"),



]
