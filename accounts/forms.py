from django import forms
from django.contrib.auth import get_user_model # User class 를 가지고 옴
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         # fields = '__all__'
#         fields = ['username', 'password']
class UserCustomCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'email')


class UserCustomChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')