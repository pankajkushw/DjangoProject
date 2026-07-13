from django import forms
from django.forms import inlineformset_factory
from .models import CandidateDetails, EducationDetails, WorkExperience


class CandidateRegistrationForm(forms.ModelForm):
    class Meta:
        model = CandidateDetails
        fields = ['first_name', 'last_name', 'user', 'date_of_birth', 'phone_number', 'address', 'city', 'state', 'country', 'zip_code']


class EducationDetailsForm(forms.ModelForm):
    class Meta:
        model = EducationDetails
        exclude = ['candidate', 'percentage']

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ['candidate']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 2. Define Formsets AFTER the forms they use are defined
EducationFormSet = inlineformset_factory(
    CandidateDetails, 
    EducationDetails, 
    form=EducationDetailsForm, # This now works
    extra=1,          
    can_delete=True   
)

WorkExperienceFormSet = inlineformset_factory(
    CandidateDetails, 
    WorkExperience, 
    form=WorkExperienceForm, # This now works
    extra=1, 
    can_delete=True
)

