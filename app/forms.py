from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper

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
    active_true = forms.BooleanField(required=False, label='Ativa')
    active_false = forms.BooleanField(required=False, label='Inativa', initial=True)

    class Meta:
        model = Call
        fields = ("__all__")
        widgets = {
            "start": forms.DateInput(format = ('%Y-%m-%d'), attrs = {'type': 'date', 'class': 'form-control'}),
            "end": forms.DateInput(format = ('%Y-%m-%d'), attrs = {'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start")
        end_date = cleaned_data.get("end")
        current_date = timezone.now().date()

        if start_date and end_date:
            if start_date >= end_date:
                self.add_error('start', 'A data de início deve ser anterior à data de término.')
            elif end_date <= current_date:
                current_date_formatted = current_date.strftime('%d/%m/%Y')
                self.add_error('end', f'A data de término deve ser maior que a data atual: {current_date_formatted}')


        active_true = cleaned_data.get('active_true')
        active_false = cleaned_data.get('active_false')

        if active_true and active_false:
            raise forms.ValidationError("Você deve marcar apenas um dos campos, Ativo ou Inativo.")

        if not active_true and not active_false:
            raise forms.ValidationError("Você deve marcar um dos campos, Ativo ou Inativo.")

        if active_true:
            institution = cleaned_data.get('institution')
            if institution:
                active_calls = Call.objects.filter(institution=institution, active=True)

                if self.instance.pk:
                    active_calls = active_calls.exclude(pk=self.instance.pk)

                if active_calls.exists():
                    raise forms.ValidationError("Já existe uma chamada ativa para esta instituição.")

        return cleaned_data


    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('active_true'):
            instance.active = True
        else:
            instance.active = False

        if commit:
            instance.save()
        return instance


    def __init__(self, *args, **kwargs):
        super(CallForm, self).__init__(*args, **kwargs)

        active_true = self.fields['active_true']
        active_false = self.fields['active_false']

        if self.instance and self.instance.pk:
            if self.instance.active:
                active_true.initial = True
                active_false.initial = False
            else:
                active_true.initial = False
                active_false.initial = True

        call_number = self.fields['number']
        call_number.widget.attrs.update({"autofocus": True})
        call_number.help_text = "A numeração tem o formato: 000/ano"

class CallActiveForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = ("active",)


class CallProductForm(forms.ModelForm):
    class Meta:
        model = CallProduct
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class CallUpdateForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = ("__all__")
        widgets = {
            "start": forms.DateInput(format = ('%Y-%m-%d'), attrs = {'type': 'date', 'class': 'form-control'}),
            "end": forms.DateInput(format = ('%Y-%m-%d'), attrs = {'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start")
        end_date = cleaned_data.get("end")
        current_date = timezone.now().date()
        if start_date and end_date:
            if start_date >= end_date:
                self.add_error('start', 'A data de início deve ser anterior à data de término.')
            elif end_date <= current_date:
                current_date_formatted = current_date.strftime('%d/%m/%Y')
                self.add_error('end', f'A data de término deve ser maior que a data atual: {current_date_formatted}')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(CallUpdateForm, self).__init__(*args, **kwargs)
        self.fields['number'].widget.attrs.update({"autofocus": True})


CallProductFormSet = inlineformset_factory(
    Call, CallProduct, form=CallProductForm,
    extra=1, can_delete=True, can_delete_extra=True
)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("institution", "call",)


class OrderedProductForm(forms.ModelForm):
    class Meta:
        model = OrderedProduct
        fields= ("call_product", "ordered_quantity",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


OrderedProductFormSet = inlineformset_factory(
    Order, OrderedProduct, form = OrderedProductForm,
    extra=1, can_delete=True, can_delete_extra=True
)


class UserCreateForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = UserCreationForm.Meta.fields + ("first_name", "institution",)

    def clean_email(self):
        email = self.cleaned_data['username']
        if UserProfile.objects.filter(username=email).exists():
            raise ValidationError(f"O email {email} já está em uso.")
        return email

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        email = self.fields['username']
        email.help_text = "Evite usar um email que já está em uso."
        email.attrs = {"autofocus": True}


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("username", "institution", "first_name",)

    def clean_email(self):
        email = self.cleaned_data['username']
        if UserProfile.objects.filter(username=email).exists():
            raise ValidationError(f"O email {email} já está em uso.")
        return email

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        email = self.fields['username']
        email.help_text = "Evite usar um email que já está em uso."
        email.attrs = {"autofocus": True}


class UserActiveForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("is_active",)
        help_texts = {'is_active': None}


class PermissionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("is_staff",)


class ConfirmPasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'autofocus':True}), label='Senha')

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

