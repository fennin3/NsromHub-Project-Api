from django.db import models

class GeneralOperationsSwitch(models.Model):
    open_action_plan = models.BooleanField(default=False)

    def __str__(self):
        return "Switch for controlling operations"
    

    
