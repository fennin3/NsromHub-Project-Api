from django.urls import path
from .views import *


urlpatterns = [
    path('create-project/', CreateProjectView.as_view(), name="create_project"),
    path("list-mp-projects/<id>/", ListProjectView.as_view(), name="list_project"),
    path("list-mp-constituent/<id>/", ListConstituentsForMpView.as_view(), name="list_project"),

    # Customized for data Tables
    path("list-mp-projects-cust/<id>/", CustomListProjectView.as_view(), name="list_project_cust"),
    # path("list-mp-constituent-cust/<id>/", ListConstituentsForMpView.as_view(), name="list_project_cust"),

    # Send Emails
    path("mp-send-emails/", SendEmailView.as_view(), name="send_mail"),
    path("mp-send-email/", SendEmailToConstView.as_view(), name="send_to_const"),



    path("mp-projects-search/<id>/<query>/", ProjectsSearchEngineView.as_view(), name="search_projects"),
    path("mp-constituent-search/<constituency>/<query>/", ConstituentsSearchEngineView.as_view(), name="search_constituent"),


    # Send message
    path("mp-send-message/", SendMessageToContView.as_view(), name="send_message"),


    # Request Notifications
    path("mp-ir/<id>", RetrieveIncidentReportView.as_view(), name="retrieve_ir"),
    path("mp-ms/<id>", RetrieveMessageView.as_view(), name="message"),
    path("mp-request-notifications/<id>/", RetrieveRequestNotificationsView.as_view(), name="request_notification"),

    # Making subadmins and setting permissions
    path("mp-make-subadmin/<id>/<subadmin_id>/", MakeSubAdminView.as_view(), name="make_subadmin"),
    path("mp-unmake-subadmin/<id>/<subadmin_id>/", UnmakeSubAdmin.as_view(), name="unmake_subadmin"),
    path("retrieve-all-subadmins/<id>/", RetrieveAllSubAdminsView.as_view(), name="make_subadmin"),

    # Action plans
    path("retrieve-action-plans-summary/<id>/<date>/", RetrieveActionPlanSummaryEachAreaForMPView.as_view(), name="ac_plan"),
    

    # creating account for others
    path("create-account-for-others/<id>/<type_>/", CreateUserAccountForOtherView.as_view(), name="create_account_for_others"),


    # Setting permissions
    path("set-permission/<subadmin_id>/", SetPermissionsForSubAdmin.as_view(), name="set_permission"),
    path("get-users-in-country/<country>/", AllUsersInACountry.as_view(), name="users"),

    # Share action plan as Post...datetime A combination of a date and a time. Attributes: ()
    path("share-action-plan/<id>/", ShareAsPostView.as_view(), name="share_as_post"),
    path("share-all-action-plan/<id>/<date>/", ShareAllAtOnce.as_view(), name="share_all_as_post"),

    # Assessment
    path("retrieve-assessment-summary/<id>/<year>/", RetrieveAssessmentView.as_view(), name="mp_assessment"),

    path("create-post/", CreatePostView.as_view(), name="create_post"),

    path("action-plan-overall-summary/<id>/<year>/", RetrieveActionPlanOverview.as_view(),name="overview"),



    path("retrieve-messages/<id>/<consti>/", RetrieveMessages.as_view(), name="retrieve_messages"),

    path("read-incident-report/<id>/", SetIncidentReportRead.as_view(), name="read_ir"),
    path("read-requestform/<id>/", SetRequestFormRead.as_view(), name="read_rf"),

    path("get-project-detail/<id>/", GetProjectDetail.as_view(), name="projectdetail"),

    path("get-areas-for-mp/<id>/", GetAreasForMP.as_view(), name="getareasformp"),
    path("send-email-to-area/<areaid>/", SendEmailToAreaView.as_view(),name="sendareaemail")
    
] 