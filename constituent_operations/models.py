from users.models import Area, Constituency
from django.db import models
from django.contrib.auth import get_user_model
from mp_operations.models import Project



User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    read = models.BooleanField(default=False)
    message = models.CharField(max_length=1000)
    attached_file = models.FileField(upload_to="message_files/", blank=True, null=True)
    date_sent = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return f"From {self.sender.full_name} To {self.receiver.email}"


class IncidentReport(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    read = models.BooleanField(default=False)
    subject = models.CharField(max_length=500, null=True, blank=True)
    message = models.CharField(max_length=20000)
    attached_file = models.FileField(upload_to="Incident_file/", blank=True, null=True) 


    def __str__(self):
        return f"Incident Report from{self.sender.full_name} to {self.receiver.full_name}"


class RequestForm(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_form_receiver")
    read = models.BooleanField(default=False)
    subject = models.CharField(max_length=500, null=True, blank=True)
    message = models.CharField(max_length=20000)
    attached_file = models.FileField(upload_to="Incident_file/", blank=True, null=True) 


    def __str__(self):
        return f"Request Form from{self.sender.full_name} to {self.receiver.full_name}"
    


# class MpsAssessment(models.Model):
#     pass


class ActionPlanToAssemblyMan(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    problem_title =models.CharField(max_length=100)
    total_participants = models.IntegerField(default=0)
    participants = models.ManyToManyField(User, null=True, blank=True)
    total_rating = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Action Plan - {self.problem_title} -- {self.date}"

    
    def avg_rating(self):
        avg = self.total_rating/self.total_participants
        return avg


class ProblemsForActionPlan(models.Model):
    title = models.CharField(max_length=10000)

class ApprovedActionPlan(models.Model):
    year = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ActionPlanParticipants(models.Model):
    year = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class  Meta:
        verbose_name_plural="Action Plan Participants"


class Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    assessment = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return f"{self.user.full_name}'s Assessment on {self.project.name}"

    
class AssessmentParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.user.full_name} - {self.year}"


class ConductsForAssessment(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"

class ConductAssessment(models.Model):
    conduct = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    assessment = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True) 

    