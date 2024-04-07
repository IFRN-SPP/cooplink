from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ("__all__")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("__all__")

class UserCreateForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = UserCreationForm.Meta.fields + ("first_name", "institution",)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("username", "first_name", "institution")
