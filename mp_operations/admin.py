from constituent_operations.models import IncidentReport, RequestForm
from django.contrib import admin
from .models import *

class ProjectAdmin(admin.ModelAdmin):
    list_display=('mp','name','is_post')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment)
admin.site.register(IncidentReport)
admin.site.register(ActionPlanAreaSummaryForMp)
admin.site.register(RequestForm)
admin.site.register(Config)
