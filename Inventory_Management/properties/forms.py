from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15, required=True)  # New field
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')  # Include phone_number in the fields

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
