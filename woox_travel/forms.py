from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

class userform(forms.Form):
    val1 = forms.CharField(label="Value 1",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    val2 = forms.CharField(label="Value 2",widget=forms.TextInput(attrs={'class':'form-control'}))

class Create_user(UserCreationForm):    
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control mb-3'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def clean_username(self):
        # Return the username without any validation
        return self.cleaned_data.get('username')
    
class Login_user(forms.Form):
    un = forms.CharField(label="Enter Username ",widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    password = forms.CharField(label="Enter Your Password ", widget=forms.PasswordInput(attrs={'class':'form-control'}))

class Update_user(UserCreationForm):    
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control mb-3'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter new password or (enter your old password)'}),required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm password'}),required=False)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def clean_username(self):
        # Return the username without any validation
        return self.cleaned_data.get('username')
    
class Change_pass(PasswordChangeForm):    
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3','placeholder': 'Enter old password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3','placeholder': 'Enter new password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-1','placeholder': 'Confirm new password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        
class Forgot_pass(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3','placeholder': 'Enter new password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-1','placeholder': 'Confirm password'}))
    
    class Meta:
        model = User
        fields = ['password1','password2']
