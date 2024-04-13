from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

from django.contrib.auth.hashers import check_password
from django.utils import timezone

from .models import *

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ("__all__")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("__all__")

class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = ("__all__")

class CallProductForm(forms.ModelForm):
    class Meta:
        model = CallProduct
        fields = ("__all__")

class UserCreateForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = UserCreationForm.Meta.fields + ("first_name", "institution",)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("username", "first_name", "institution")

# Form de Permissão
class PermissionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("is_staff",)

# Form de Confirmação de Senha
class ConfirmPasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        fields = ('confirm_password', )

    def clean(self):
        cleaned_data = super(ConfirmPasswordForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            self.add_error('confirm_password', 'Senha não corresponde.')

    def save(self, commit=True):
        user = super(ConfirmPasswordForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user
    

