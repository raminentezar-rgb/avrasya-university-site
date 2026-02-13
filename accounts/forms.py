from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2')
