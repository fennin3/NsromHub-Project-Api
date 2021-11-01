from constituent_operations.models import IncidentReport, RequestForm
from django.contrib import admin
from .models import *


admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(IncidentReport)
admin.site.register(ActionPlanAreaSummaryForMp)
admin.site.register(RequestForm)
admin.site.register(Config)
