from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where emial  is uniqe identifieer
    """
    def create_user(self, email, password,  **extra_fieldss):
        """
        create and save User with the given email and password
        """
        if not email:
            raise ValueError("Email musst be set")
        
        user = self.model(email=email, **extra_fieldss)
        user.set_password(password)

        return user;

    def create_super_user(self, email, password, **extra_fields):
        """
        Create and save a super user with given email and password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)


        if extra_fields.get("is_stuff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        user = self.create_user(email, password, **extra_fields)

   




        
