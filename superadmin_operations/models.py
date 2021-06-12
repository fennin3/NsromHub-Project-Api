from django.db import models

class GeneralOperationsSwitch(models.Model):
    open_action_plan = models.BooleanField(default=False)
    open_forum = models.BooleanField(default=False)
    open_assessment = models.BooleanField(default=False)
    

    def __str__(self):
        return "Switch for controlling operations"
    

    
