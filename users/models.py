from django.conf import settings
from django.core.exceptions import ValidationError 
from django.db import models
from django.contrib.auth.models import AbstractUser



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


    class Meta:
        verbose_name_plural ="Constituencies"

    def __str__(self):
        return self.name

    

class CustomUser(AbstractUser):
    is_mp = models.BooleanField(default=False)
    is_constituent = models.BooleanField(default=False)
    is_security_person = models.BooleanField(default=False)
    is_medical_center = models.BooleanField(default=False)
    full_name = models.CharField(max_length=250)
    email = models.EmailField()
    contact = models.CharField(max_length=16, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="members", null=True, blank=True)
    region = models.ManyToManyField(Region, null=True, blank=True, related_name="members")
    constituency = models.ManyToManyField(Constituency, related_name="members")
    system_id_for_user = models.CharField(max_length=15, null=True, blank=True)





    def __str__(self):
        return self.email


class Constituent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    voters_id = models.CharField(max_length=50)
    town = models.CharField(max_length=100)
    is_subadmin = models.BooleanField(default=False)
    
    


    def __str__(self):
        return self.user.full_name





    def __str__(self):
        return self.user.full_name
    

    




class MpProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    mp_id = models.CharField(max_length=50)
    


    def __str__(self):
        return self.user.full_name



class SubAdminPermission(models.Model):
    sub_admin = models.OneToOneField(Constituent, on_delete=models.CASCADE)
    can_post_projects = models.BooleanField(default=True)
    can_read_requests = models.BooleanField(default=True)
    can_send_emails = models.BooleanField(default=True)
    sub_admin_for = models.ForeignKey(MpProfile, on_delete=models.CASCADE, blank=True, null=True)
