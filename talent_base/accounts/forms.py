from django import forms
from django.forms import inlineformset_factory
from .models import CandidateDetails, EducationDetails, WorkExperience

class CandidateDetailsForm(forms.ModelForm):
    class Meta:
        model = CandidateDetails
        # Exclude system-handled fields like user and registration_number
        exclude = ['user', 'registration_number']

class EducationDetailsForm(forms.ModelForm):
    class Meta:
        model = EducationDetails
        exclude = ['candidate', 'percentage'] # percentage is auto-calculated in save()

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ['candidate']

# --- Inline Formsets for Multiple Dynamic Rows ---

EducationFormSet = inlineformset_factory(
    CandidateDetails, 
    EducationDetails, 
    form=EducationDetailsForm,
    extra=1,          # Number of blank forms to show initially
    can_delete=True   # Allows users to check a box to delete rows
)

WorkExperienceFormSet = inlineformset_factory(
    CandidateDetails, 
    WorkExperience, 
    form=WorkExperienceForm,
    extra=1, 
    can_delete=True
)
