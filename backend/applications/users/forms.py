# accounts/forms.py
from django import forms
from .models import Profile
from datetime import date

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'date_of_birth', 'bio']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),  # HTML5 date picker
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            if dob > today:
                raise forms.ValidationError("Date of birth cannot be in the future.")
            
            # Optional: Minimum age (e.g., 18)
            age = today.year - dob.year
            if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
                age -= 1
            if age < 18:
                raise forms.ValidationError("You must be at least 18 years old.")
        
        return dob
    

class CustomSignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    avatar = forms.ImageField(
        help_text="Your Avatar",
        required=True
    )

    def signup(self, request, user):
        """Called after user is created but before saved to handle additional fields"""
        user.firt_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data.get('last_name')

        user.save()

        profile = Profile.objects.create(user=user)
        profile.avatar = self.cleaned_data['avatar']
        profile.save()