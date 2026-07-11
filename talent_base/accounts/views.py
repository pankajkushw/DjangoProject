
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import CandidateDetails, User, PendingUser, Token, TokenType
from django.contrib import messages, auth
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone
from accounts.common.tasks import send_email
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .forms import CandidateDetailsForm, WorkExperienceFormSet
import quopri
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import CandidateDetailsForm, EducationFormSet, WorkExperienceFormSet


# Create your views here.
def home(request: HttpRequest):
    return render(request, "home.html")

def login(request: HttpRequest):

    if request.method == "POST":
        email:str = request.POST.get("email")
        password:str = request.POST.get("password")
        messages.error(request, "reached login")
        user = auth.authenticate(request, email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Account verified. Welcome to entry page !!")
            return redirect("recurtiment_data_input") # if successful login, redirect to the recurtiment_data_input page
        else: 
            messages.error(request, "Invalid credentials")
            return redirect("login")

    else:
        return render(request, "login.html")

def logout(request: HttpRequest):
    auth.logout(request)
    messages.success(request, "You are now loged out")
    return redirect("home")


def register(request: HttpRequest):

    if request.method == "POST":
        email: str = request.POST["email"]
        password : str = request.POST["password"]
        cleaned_email = email.lower()

        if User.objects.filter(email=cleaned_email).exists():
            messages.error(request, "email ID exist, Please login using your credentials.")
            return redirect("login")
        else:
            verification_code = get_random_string(10)
            PendingUser.objects.update_or_create(
                email = cleaned_email,
                defaults= {
                    "password":make_password(password),
                    "verification_code": verification_code,
                    "created_at": datetime.now(timezone.utc),
                }
            )
            send_email(
                "Verify your account",
                [cleaned_email],
                "emails/email_verification_template.html",
                context={"code": verification_code}
            )
            messages.success(request, f"Verification code sent to {cleaned_email}")
            return render(request, "verify_account.html", context={"email":cleaned_email})
    else:
        return render(request, "register.html")
    
def verify_account(request: HttpRequest):
    if request.method == "POST":
        email:str = request.POST["email"]

        if "code" in request.POST:
            v_code = request.POST["code"]
        else:
            v_code = ""
        
        pending_user: PendingUser = PendingUser.objects.filter(
            verification_code = v_code, email = email
        ).first()
        
        if pending_user and pending_user.is_valid():
            user = User.objects.create(
                email = pending_user.email, password = pending_user.password
            )
            pending_user.delete()
            auth.login(request, user)
            messages.success(request, "Account verified. Please login again to submit your details!!")
            return redirect("logout")
        else:
            messages.error(request, "Invalid or expired verification code")
            return render(request, "verify_account.html", context = {"email": email}, status=400)
        
def send_password_reset_link(request: HttpRequest):
    if request.method == "POST":
        email: str = request.POST.get("email","")
        user = get_user_model().objects.filter(email=email.lower()).first()

        if user:
            token, _ = Token.objects.update_or_create(
                user=user,
                token_type = TokenType.PASSWORD_RESET,
                defaults= {
                    "token": get_random_string(20),
                    "created_at": datetime.now(timezone.utc),
                }
            )
            domain = request.get_host()
            email_data = {
                "email": email.lower(),
                "token": token.token,
                "reset_link": f"http://{domain}/auth/verify_password_reset_link/{email.lower()}/{token.token}/"
            }
            messages.info(request, "Sending password reset link to your email... { token: " + token.token + " }")
            send_email(
                "Your password reset link",
                [email],
                "emails/password_reset_template.html",
                email_data
            )
            messages.success(request, "reset link sent to your email, please check your inbox and spam folder.")
            return redirect("login")  # Redirect to the login page after sending the email
        else:
            messages.error(request, "email not found, please register first.")
            return redirect("register")
    else:
        return render(request, "forgot_password.html")
    
def verify_password_reset_link(request: HttpRequest, email: str, reset_token: str):
    # 1. Safely decode Quoted-Printable terminal wrapping
    if email:
        try:
            email = quopri.decodestring(email.encode("utf-8")).decode("utf-8")
            email = email.strip()
        except Exception:
            pass

    if reset_token:
        try:
            reset_token = quopri.decodestring(reset_token.encode("utf-8")).decode(
                "utf-8"
            )
            reset_token = reset_token.strip().rstrip("/")
        except Exception:
            pass

    # 2. Run the database lookup
    token = Token.objects.filter(
        user__email=email, token=reset_token, token_type=TokenType.PASSWORD_RESET
    ).first()

    # 3. Handle invalid or expired token cases
    if not token or not token.is_valid():
        messages.error(request, "Invalid or expired reset link")
        return redirect("send_password_reset_link")

    # 4. Handle Password Update (POST)
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            # Always pass the CLEANED variables back to the template
            return render(
                request,
                "verify_password_reset_link.html",
                context={"email": email, "token": reset_token},
            )

        # TODO: Add password strength validation here (e.g., length check)

        # Save new password safely
        user = token.user
        user.set_password(new_password)
        user.save()

        # Burn token after single use
        token.delete()

        messages.success(
            request, "Password reset successful. Please login with your new password."
        )
        return redirect("login")

    # 5. Render the page form on a standard GET request
    return render(
        request,
        "verify_password_reset_link.html",
        context={"email": email, "token": reset_token},
    )
@login_required
def create_candidate_profile_view(request):
    # 1. Fetch the existing database profile row for this logged-in user
    existing_profile = CandidateDetails.objects.filter(user=request.user).first()

    if request.method == 'POST':
        # FIX: Pass instance=existing_profile to force an UPDATE instead of a duplicate INSERT
        candidate_form = CandidateDetailsForm(request.POST, request.FILES, instance=existing_profile)
        
        # FIX: Explicitly set the prefixes to match your HTML template targets exactly
        education_formset = EducationFormSet(request.POST, request.FILES, instance=existing_profile, prefix='educations')
        experience_formset = WorkExperienceFormSet(request.POST, request.FILES, instance=existing_profile, prefix='experiences')
        
        # 2. Check validity of ALL forms together
        if candidate_form.is_valid() and education_formset.is_valid() and experience_formset.is_valid():
            candidate = candidate_form.save(commit=False)
            candidate.user = request.user
            
            if not candidate.registration_number:
                # Generate a unique registration number if it doesn't exist
                candidate.registration_number = f"REG-{request.user.id}-{int(datetime.now().timestamp())}"

            with transaction.atomic():
                candidate.save() # Saves profile (updates if exists, creates if new)
                
                # Re-bind the freshly saved profile instance to your formsets before execution
                education_formset.instance = candidate
                experience_formset.instance = candidate
                
                education_formset.save()
                experience_formset.save()
                
            # FIX: Removed whitespace from the redirect URL configuration pattern string
            return redirect('profile_success_view')
            
    else:
        # FIX: Pass instance=existing_profile on GET requests to populate old data if it exists
        candidate_form = CandidateDetailsForm(instance=existing_profile)
        education_formset = EducationFormSet(instance=existing_profile, prefix='educations')
        experience_formset = WorkExperienceFormSet(instance=existing_profile, prefix='experiences')

    context = {
        'candidate_form': candidate_form,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
    }
    return render(request, 'recurtiment_input.html', context)


@login_required
def profile_success_view(request):
    # FIX: Query using the model name (CandidateDetails) instead of the form class (CandidateDetailsForm)
    candidate = CandidateDetails.objects.filter(user=request.user).first()
    
    context = {
        'candidate': candidate,
        # Use the custom related_name parameters from your models.py
        'educations': candidate.educations.all() if candidate else [],
        'experiences': candidate.experiences.all() if candidate else [],
    }
    return render(request, 'profile_preview.html', context)