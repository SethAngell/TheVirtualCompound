from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser, Invitation


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "name",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "name",
        )


class NewInvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ("linked_domain", "email")


class NewUserFromInviteForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=128)
    invite_code = forms.CharField(max_length=128)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
