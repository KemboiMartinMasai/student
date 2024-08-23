from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    class Meta:
        model=User
        fields=['username','email','password1','password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.profile.phone_number = self.cleaned_data['phone_number']
            user.profile.save()
        return user

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['adm_number','first_name', 'gender','last_name', 'email','phone_number', 'enrollment_date','date_of_birth', 'profile_picture']