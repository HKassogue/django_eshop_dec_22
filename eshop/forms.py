from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('D', 'Direct Check'),
    ('B', 'Bank Transfer'),
)

class CheckOutForm(forms.Form):        
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}))
    country = CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100', }))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your state'}))
    zipcode = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your zip code'}))
    
    payment_option = forms.ChoiceField( widget=forms.RadioSelect, choices=PAYMENT_CHOICES)