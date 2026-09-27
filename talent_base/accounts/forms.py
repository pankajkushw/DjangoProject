from email.headerregistry import Address

from django import forms
from django.forms import inlineformset_factory
from .models import CandidateDetails, WorkExperience, EducationDetails


STATE_CHOICE = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
)

class CandidateRegistrationForm(forms.ModelForm):
    class Meta:
        model = CandidateDetails
        fields = [
            'first_name', 'last_name', 'father_name', 'mother_name', 'date_of_birth', 
            'phone_number', 'email_id', 'address', 'city', 'state', 'country', 'zip_code']

        labels = {
            'first_name':'First Name',
            'last_name': 'Last Name',
            'father_name': 'Father Name',
            'mother_name': 'Mother Name',
            'date_of_birth': 'Date of Birth',
            'phone_number': 'Phone Number',
            'email_id': 'Email ID',
            'address': 'Address',
            'city': 'City',
            'state': 'State',
            'country': 'Country',
            'zip_code': 'Pin Code'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'father_name':forms.TextInput(attrs={'class':'form-control'}),
            'mother_name':forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'id':'datepicker', 'type':'date'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control'}),
            'email_id':forms.EmailInput(attrs={'class':'form-control'}),
            'address':forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(choices=STATE_CHOICE, attrs={'class':'form-control'}),
            'country':forms.TextInput(attrs={'class':'form-control'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control'})
            
        }

        

class EducationDetailsForm(forms.ModelForm):
    class Meta:
        model = EducationDetails
        fields = [
            'degree', 'institution', 'university', 'year_completed', 'marks_obtained', 
            'total_marks' ]

        labels = {
            'degree': 'Degree',
            'institution': 'Institution',
            'university': 'University',
            'year_completed': 'Year of Completion',
            'marks_obtained': 'Marks Obtained',
            'total_marks': 'Total Marks',
        }
        widgets = {
            'degree': forms.TextInput(attrs={'class':'form-control'}),
            'institution': forms.TextInput(attrs={'class':'form-control'}),
            'university': forms.TextInput(attrs={'class':'form-control'}),
            'year_completed': forms.NumberInput(attrs={'class':'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={'class':'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class':'form-control'}),
            'percentage': forms.NumberInput(attrs={'class':'form-control'})
        }
class WorkExperienceForm(forms.ModelForm):
    
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'position', 'start_date', 'end_date']
        labels = {
            'company_name': 'Name of Institution/Company',
            'position': 'Position/Role',
            'start_date': 'Start Date',
            'end_date': 'End Date',
        }
        widgets = {
            'company_name': forms.TextInput(attrs={'class':'form-control'}),
            'position': forms.TextInput(attrs={'class':'form-control'}),
            'start_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'end_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        } 
