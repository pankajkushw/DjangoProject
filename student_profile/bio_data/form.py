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
    class Meta:
        model = Profile
        fields = 