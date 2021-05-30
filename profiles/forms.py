from django import forms
from .models import Profile

class ProfileModelForm(forms.ModelForm):  # form for update profiles
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name','mobile','email','avatar')
