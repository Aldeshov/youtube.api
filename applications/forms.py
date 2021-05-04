from django import forms

from applications.models import Profile


class PersonForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = '__all__'
