from django import forms
from django.forms import inlineformset_factory
from .models import CandidateDetails, EducationDetails, WorkExperience

class CandidateDetailsForm(forms.ModelForm):
    class Meta:
        model = CandidateDetails
        exclude = ['user', 'registration_number']
        widgets = {
            # Injects native calendar option in the candidate personal details block
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class EducationDetailsForm(forms.ModelForm):
    class Meta:
        model = EducationDetails
        exclude = ['candidate', 'percentage']

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ['candidate']
        widgets = {
            # Injects native calendars inside the dynamic row layout elements
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# --- Inline Formsets for Multiple Dynamic Rows ---

EducationFormSet = inlineformset_factory(
    CandidateDetails, 
    EducationDetails, 
    form=EducationDetailsForm,
    extra=1,          
    can_delete=True   
)

WorkExperienceFormSet = inlineformset_factory(
    CandidateDetails, 
    WorkExperience, 
    form=WorkExperienceForm,
    extra=1, 
    can_delete=True
)
