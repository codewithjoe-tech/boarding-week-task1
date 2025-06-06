from django.contrib.auth.models import BaseUserManager



class CustomUserManager(BaseUserManager):
    def create_user(self , email , password=None , **extra):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email , **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email , password=None, **extra):
        extra.setdefault("is_superuser" , True)
        extra.setdefault("is_staff" , True)
        return self.create_user(email , password, **extra)
    