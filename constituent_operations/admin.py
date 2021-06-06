from django.contrib import admin
from .models  import *


admin.site.register(Message)
admin.site.register(ActionPlanToAssemblyMan)
admin.site.register(ProblemsForActionPlan)
admin.site.register(ApprovedActionPlan)
admin.site.register(ActionPlanParticipants)
admin.site.register(AssessmentParticipant)
admin.site.register(Assessment)
admin.site.register(ConductAssessment)
admin.site.register(ConductsForAssessment)
