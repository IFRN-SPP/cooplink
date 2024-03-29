from django import forms
from .models import *


class InstitutionForm(forms.ModelForm):
    
    class Meta:
        model = Institution
        fields = ("__all__")

