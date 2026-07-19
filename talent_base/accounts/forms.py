from django import forms
from django.forms import inlineformset_factory
from .models import CandidateDetails, EducationDetails, WorkExperience


class CandidateRegistrationForm(forms.ModelForm):
    class Meta:
        model = CandidateDetails
        fields = [
            'first_name', 'last_name', 'user', 'date_of_birth', 
            'phone_number', 'address', 'city', 'state', 'country', 'zip_code'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class EducationDetailsForm(forms.ModelForm):
    class Meta:
        model = EducationDetails
        exclude = ['candidate', 'percentage']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Loop to automatically apply Bootstrap styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ['candidate']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap styling while preserving existing widget attributes
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            new_classes = f"{existing_classes} form-control".strip()
            field.widget.attrs.update({'class': new_classes})

EducationFormSet = inlineformset_factory(
    CandidateDetails, 
    EducationDetails, 
    form=EducationDetailsForm, 
    extra=1,          
    can_delete=True   
)

# Custom initialization logic if you need to pass it directly to the wizard steps
class BaseEducationFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure management form fields or deletion checkboxes get styled if neede

# Define Formset AFTER the forms they use are defined
WorkExperienceFormSet = inlineformset_factory(
    CandidateDetails, 
    WorkExperience, 
    form=WorkExperienceForm, 
    extra=1, 
    can_delete=True
)

