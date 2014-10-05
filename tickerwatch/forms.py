from django import forms
from tickerwatch.models import UserProfile, Stock
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())

  def __init__(self, *args, **kwargs):
    super(UserForm, self).__init__(*args, **kwargs)

    for fieldname in ['username', 'password',]:
      self.fields[fieldname].help_text = None

  class Meta:
    model = User
    fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = ('phone_number',)

class StockForm(forms.ModelForm):
  class Meta:
    model = Stock
    fields = ('ticker',)

class TextForm(forms.ModelForm):
  class Meta:
      model = Stock
      fields = ('ticker',)

class TextDemoForm(forms.ModelForm):
  class Meta:
      model = Stock
      fields = ('ticker',)
