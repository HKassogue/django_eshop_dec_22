from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, 
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    password = forms.CharField(max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))