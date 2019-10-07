from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from market.models import UserInfo

class UserInfoCreationForm(UserCreationForm):

    class Meta:
        model = UserInfo
        fields = ('username', 'email')

class UserInfoChangeForm(UserChangeForm):

    class Meta:
        model = UserInfo
        fields = ('username', 'email')