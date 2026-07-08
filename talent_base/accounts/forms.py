from django import forms
from django.forms import inlineformset_factory
from .models import CandidateDetails, WorkExperience

class CandidateDetailsForm(forms.ModelForm):
    class Meta:
        model = CandidateDetails
        # Excluding 'user' as it will be injected automatically via the view
        exclude = ['user']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter father's name"}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter mother's name"}),
            'category': forms.RadioSelect(), # Overridden by your custom template HTML structure
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ['candidate']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Google'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Developer'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# Generate a structural Inline Formset link mapping WorkExperience to CandidateDetails
WorkExperienceFormSet = inlineformset_factory(
    CandidateDetails,
    WorkExperience,
    form=WorkExperienceForm,
    extra=1,            # Start with 1 blank row layout natively
    can_delete=True,     # Allows row removal handling 
)
