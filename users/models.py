from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

def validate_dob(value):
    """Ensure date_of_birth is not in the future and user is at least 13 years old."""
    today = date.today()
    if value > today:
        raise ValidationError("Date of birth cannot be in the future.")
    
    # Optional: Minimum age check (e.g., 13 years)
    # age = today.year - value.year
    # if today.month < value.month or (today.month == value.month and today.day < value.day):
    #     age -= 1
    # if age < 13:
    #     raise ValidationError("User must be at least 13 years old.")
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_of_birth = models.DateField(
        null=True, 
        blank=True,
        validators=[validate_dob]  # Apply the validator here
    )
    bio = models.TextField(max_length=500, blank=True)

    def clean(self):
        """Override for additional model-wide validation if needed."""
        super().clean()
        # Call your validator explicitly if not using field validators
        if self.date_of_birth:
            validate_dob(self.date_of_birth)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
