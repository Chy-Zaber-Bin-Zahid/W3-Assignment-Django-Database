from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=15, required=True)  # New field
    last_name = forms.CharField(max_length=15, required=True)  # New field
    

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
