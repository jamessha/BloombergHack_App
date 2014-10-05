from django import forms
from tickerwatch.models import UserProfile, Stock
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User
    fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = ('picture',)

class StockForm(forms.ModelForm):
  class Meta:
    model = Stock
    fields = ('ticker',)

