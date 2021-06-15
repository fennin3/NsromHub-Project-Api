from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _



class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural ="Countries"

    def __str__(self):
        return self.name
    

class Region(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name="regions")

 
    def __str__(self):
        return self.name


class Constituency(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True, related_name="constituencies")
    description = models.CharField(max_length=50000, null=True, blank=True)
    image = models.ImageField(upload_to="contistituency_image/", default="")

    class Meta:
        verbose_name_plural ="Constituencies"

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Constituency, on_delete=models.CASCADE, blank=True, null=True, related_name="towns")


    class Meta:
        verbose_name_plural ="Towns"

    def __str__(self):
        return self.name



class Area(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Town, on_delete=models.CASCADE, blank=True, null=True, related_name="areas")


    class Meta:
        verbose_name_plural ="Areas"

    def __str__(self):
        return self.name
    

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    is_mp = models.BooleanField(default=False)
    is_constituent = models.BooleanField(default=False)
    is_security_person = models.BooleanField(default=False)
    is_medical_center = models.BooleanField(default=False)
    is_assembly_man = models.BooleanField(default=False)
    full_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField()
    contact = models.CharField(max_length=16, default="")
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="members", null=True, blank=True)
    region = models.ManyToManyField(Region, null=True, blank=True, related_name="members")
    constituency = models.ManyToManyField(Constituency, related_name="members")
    system_id_for_user = models.CharField(max_length=15, null=True, blank=True)
    phone_verified = models.BooleanField(default=False)
    active_constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, blank=True, null=True)
    active_town = models.ForeignKey(Town, on_delete=models.CASCADE, blank=True, null=True)
    active_area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="user_profile_pics/", blank=True, null=True, default="default.jpg")
    is_subadmin = models.BooleanField(default=False)
    subadmin_for = models.ForeignKey(Constituency, null=True, blank=True, on_delete=models.CASCADE, related_name="subadmins")
    email_verified = models.BooleanField(default=False)
    REQUIRED_FIELDS = []

    # class Meta:
    #     unique_together = ('email', 'contact',)





    def __str__(self):
        return self.email


class Constituent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="more_info")
    voters_id = models.CharField(max_length=50)
    arr = models.CharField(max_length=100)
    town = models.ManyToManyField(Town, related_name="members", null=True, blank=True)
    area = models.ManyToManyField(Area, related_name="members", null=True, blank=True)
    is_subadmin = models.BooleanField(default=False)
    subadmin_for = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="sub_admins")
    
    


    def __str__(self):
        return self.user.full_name

    def __str__(self):
        return self.user.full_name
   

class MpProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name="mp_profile")
    mp_id = models.CharField(max_length=50)
    


    def __str__(self):
        return self.user.full_name



class SubAdminPermission(models.Model):
    sub_admin = models.OneToOneField(Constituent, on_delete=models.CASCADE, related_name="permissions")
    can_post_projects = models.BooleanField(default=True)
    can_read_requests = models.BooleanField(default=True)
    can_send_emails = models.BooleanField(default=True)
    can_reply_messages = models.BooleanField(default=True)
    can_read_incident = models.BooleanField(default=True)
    sub_admin_for = models.ForeignKey(MpProfile, on_delete=models.CASCADE, blank=True, null=True)



class OTPCode(models.Model):
    code_for = models.CharField(max_length=100)
    code = models.CharField(max_length=7)


class Permission(models.Model):
    name = models.CharField(max_length=5000)

    def __str__(self):
        return self.name


class UserPermissionCust(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    permission_name = models.CharField(max_length=5000, null=True, blank=True)
    permission_value = models.BooleanField(default=False) 


    def __str__(self):
        return self.permission_name
    
