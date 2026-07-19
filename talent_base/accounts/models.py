from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from .manager import CustomUserManager
from datetime import datetime, timezone
from accounts.common.models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.core.exceptions import ValidationError
# Create your models here.

# accounts/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

class PendingUser(BaseModel):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60
        now = datetime.now(timezone.utc)
        timediff = now - self.created_at
        timediff = timediff.total_seconds()
        if timediff > lifespan_in_seconds:
            return False
        return True
    
class TokenType(models.TextChoices):
    PASSWORD_RESET = ("PASSWORD_RESET")

class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=100, choices= TokenType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.token}"
    
    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60
        now = datetime.now(timezone.utc)
        timediff = now - self.created_at
        timediff = timediff.total_seconds()
        if timediff > lifespan_in_seconds:
            return False
        return True
    

# Base abstract model assuming you have a custom BaseModel handling created_at/updated_at

class CandidateDetails(BaseModel):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('OBC-NCL', 'OBC (Non-Creamy Layer)'),
        ('SC', 'Scheduled Caste'),
        ('ST', 'Scheduled Tribe'),
    ]
    registration_number = models.CharField(max_length=100, unique=True, auto_created=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Kept if separate from auth user names, otherwise remove and use user.first_name
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    
    # File attachments (Make blank=True if they don't upload them instantly on step 1)
    date_of_birth_certificate = models.FileField(upload_to='dob_certificates/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    category_certificate = models.FileField(upload_to='category_certificates/', blank=True, null=True)
    
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.email})"

    
def current_year():
    return datetime.now().year

def year_choices():
# Counts backward from (Current Year + 5) down to 1950
    return [(r, r) for r in range(current_year(), 1980, -1)]


class EducationDetails(BaseModel):
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    year_completed = models.PositiveIntegerField(
        choices=year_choices(),
        default=current_year,  # Removed parentheses () so it evaluates on creation, not migration
        validators=[
            MinValueValidator(1980),
            MaxValueValidator(current_year())
        ]
    )

    marks_obtained = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    percentage = models.FloatField(editable=False) 
    degree_certificate = models.FileField(upload_to='degree_certificates/', blank=True, null=True)


    def save(self, *args, **kwargs):
        # Enforce backend auto-calculation
        if self.total_marks > 0:
            self.percentage = round((self.marks_obtained / self.total_marks) * 100, 2)
        else:
            self.percentage = 0.0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.degree} - {self.institution}"

class WorkExperience(BaseModel):
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    
    # Nullable end_date to support "Currently Working Here" states
    end_date = models.DateField(null=True, blank=True) 
    responsibilities = models.TextField(blank=True)
    experience_certificate = models.FileField(upload_to='experience_certificates/', blank=True, null=True) 

    def clean(self):
        super().clean()
        # Prevent chronologically impossible setups
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': "End date cannot be earlier than the start date."})

    def save(self, *args, **kwargs):
        self.full_clean()  # Forces full validation before saving to the database
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.position} at {self.company_name}"


