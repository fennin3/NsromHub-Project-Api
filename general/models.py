from django.db import models
from django.contrib.auth import get_user_model
from users.models import Constituency

User = get_user_model()


class ForumMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owners")
    message = models.CharField(max_length=40000)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    current_mp = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mp")
    date_sent = models.DateTimeField(auto_now_add=True, blank=True, null=True)
