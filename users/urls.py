from users.serializers import ListAllCountriesSerializer
from django.urls import path
from . import views

urlpatterns = [
    # Login - Register
    path("create-constituent-account/", views.ConstituentCreateApiView.as_view(), name="createconstituent"),
    path("create-mp-account/<id>/", views.MPCreateApiView.as_view(), name="createmp"),
    path("create-secondary-account/", views.SecondaryRegistration.as_view(), name="secondary_create"),

    # Listing 
    path('all-countries/', views.RetrieveAllCountriesView.as_view(), name="all_countries"),


    # Verifications
    path('email-otp-verification/', views.OTPEmailVerificationView.as_view(), name="verify_email"),
    path('get-phone-verification/', views.GetOTPSMSView.as_view(), name="verify_phone"),
    path('phone-verify/', views.OTPPhoneVerificationView.as_view(), name="verify_phone"),

    path("send-reset-code/<email>/", views.ForgotPasswordEmailVerify.as_view(), name="aa"),
    path("check-code/<uuid>/",views.CheckCode.as_view(), name="qaqq"),
    path("password-reset", views.SetPassword.as_view(), name="yy2")
    # temp

]
