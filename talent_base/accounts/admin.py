from django.contrib import admin
from .models import User, PendingUser, CandidateDetails, EducationDetails, WorkExperience
# Register your models here.
admin.site.register(User)
admin.site.register(PendingUser)
admin.site.register(CandidateDetails)
admin.site.register(EducationDetails)
admin.site.register(WorkExperience)
