from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group 

class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signUp.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and extra data
            # You can add user to a group (e.g., 'Property Owners')
            property_owners_group = Group.objects.get(name='Property Owners')
            user.groups.add(property_owners_group)
            login(request, user)
            return redirect('admin:login')  # Redirect to admin login after successful sign up
        return render(request, 'signUp.html', {'form': form})
