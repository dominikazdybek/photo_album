from django import forms
from .models import Photo
from django.forms import Form, ModelForm
from django.core.validators import EmailValidator
from django.contrib.auth.models import User


class LoginForm(Form):
    username = forms.CharField(label="Login", max_length=64,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Hasło", max_length=64, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))


class RegisterForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Hasło', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Hasło (ponownie)', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Imię',widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Nazwisko', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}),
                            validators=[EmailValidator(), ])

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.errors['password1'] = self.error_class(['Podane hasła nie są jednakowe'])

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Login zajęty")
        return username


class UploadFileForm(forms.Form):
    image = forms.FileField(label='Add photo')


class CommentForm(Form):
    content = forms.CharField(label="", max_length=64,
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': 'Dodaj komentarz'}))
