from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=15,min_length=4,widget=forms.TextInput())
    last_name = forms.CharField(max_length=15,min_length=4,widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    phone = forms.CharField(max_length=10,min_length=10,widget=forms.NumberInput())
    class Meta:
        model = User
        fields = ('first_name','last_name','email','phone','username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=15,min_length=4,widget=forms.TextInput())
    last_name = forms.CharField(max_length=15,min_length=4,widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    phone = forms.CharField(max_length=10,min_length=10,widget=forms.NumberInput())
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':True}))
    class Meta:
        model = User
        fields = ('first_name','last_name','email','phone','username')