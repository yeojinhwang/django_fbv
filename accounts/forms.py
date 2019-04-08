from django import forms
from django.contrib.auth import get_user_model

class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        # fields = '__all__'
        fields = ['username', 'password']