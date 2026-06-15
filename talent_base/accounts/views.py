from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import User, PendingUser
from django.contrib import messages, auth
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone
from accounts.common.tasks import send_email


# Create your views here.
def home(request: HttpRequest):
    return render(request, "home.html")


def register(request: HttpRequest):
    if request.method == "POST":
        email: str = request.POST["email"]
        password : str = request.POST["password"]
        cleaned_email = email.lower()

        if User.objects.filter(email=cleaned_email).exists():
            messages.error("Email exist on the platform")
            return redirect("register")
        else:
            verfication_code = get_random_string(10)
            PendingUser.objects.update_or_create(
                email = cleaned_email,
                defaults= {
                    "password":make_password(password),
                    "verification_code": verfication_code,
                    "created_at": datetime.now(timezone.utc)

                }
            )
            send_email(
                "Verify your account",
                [cleaned_email],
                "emails/email_verification_template.html",
                context={"code": verfication_code}
            )
            messages.success(request, f"Verification code sent to {cleaned_email}")
            return render(request, "verify_account.html", context={"email":cleaned_email})
    else:
        return render(request, "register.html")
    
def verify_account(request: HttpRequest):
    if request.method == "POST":
        code:str = request.POST["code"]
        email: str = request.POST["email"]
        pending_user: PendingUser = PendingUser.objects.filter(
            verification_code = code, email = email
        ).first()
        
        if pending_user and pending_user.is_valid():
            user = User.objects.create(
                email = pending_user.email, password = pending_user.password
            )
            pending_user.delete()
            auth.login(request, user)
            messages.success(request, "Account verified. You are loged in!!")
            return redirect("home")
        else:
            messages.error(request, "Invalid or expired verification code")
            return render(request, "verify_account.html", {"email": email}, status=400)