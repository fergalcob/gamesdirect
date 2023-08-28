from django import forms

class SignUpForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=128)