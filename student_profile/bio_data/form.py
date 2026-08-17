from django import forms
from bio_data.models import Profile

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
)

JOB_CITY_CHOICE = [
    ('Delhi', 'Delhi'),
    ('Pune', 'Pune'),
    ('Mumbai', 'Mumbai'),
    ('Raipur', 'Raipur'),
    ('Bangalore', 'Bangalore')
]

class ProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect,
    )
    job_city = forms.MultipleChoiceField(
        choices=JOB_CITY_CHOICE,
        widget=forms.CheckboxSelectMultiple,
        label="Preferred Job Cities",
        help_text="Select one or more cities where you prefer to work."
    )

    class Meta:
        model = Profile
        fields = [ 'name', 'dob', 'gender', 'locality', 'city', 
                  'pin', 'state', 'mobile', 'email','job_city', 'profile_image', 
                  'my_file']

        labels = {
            'name': 'Full Name',
            'dob': 'Date of Birth',
            'pin': 'Pin Code',
            'mobile': 'Mobile Number'
        }
        help_texts = {
            'profile_image': " Optional: Upload required documents"
            ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'id':'datepicker', 'type':'date'}),
            'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your area name.'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your city name.'}),
            'pin': forms.NumberInput(attrs={'class':'form-select', 'placeholder':'6-digit PIN code.'}),
            'state': forms.Select(attrs={'class':'form-select'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'10-digit mobile number.'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email Address.'})
           
        }