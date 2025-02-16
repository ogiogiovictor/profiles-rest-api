from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin





from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
        
# Create your models here.
class UserProfileManager(BaseUserManager):
    """
    Manager for UserProfile.
    """
    #def create_user(self, email, name, password=None):
    def create_user(self, email, name, password=None, user_type=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    #def create_superuser(self, email, name, password):
    def create_superuser(self, email, name, password, user_type="admin"):
        """
        Create and return a superuser.
        """
        #user = self.create_user(email, name, password)
        user = self.create_user(email, name, password, user_type)
        user.is_staff = True
        user.is_superuser = True
        user.user_type = 'agent' # remove this later 
        user.save(using=self._db)

        return user
    
    
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email and name fields.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(default="agent", max_length=255)

    objects = UserProfileManager()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name.split()[0] if self.name else ""
        #return self.name
        
    def save(self, *args, **kwargs):
        """Ensure email is always saved in lowercase."""
        self.email = self.email.lower()
        super().save(*args, **kwargs)
    
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class ProfileFeedItem(models.Model):
    #user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_profile.name} - {self.status_text}"
    
    class Meta:
        verbose_name = "Profile Feed Item"
        verbose_name_plural = "Profile Feed Items"
        ordering = ['-created_at']
        