from django import forms

from bakery.profiles.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
