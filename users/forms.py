from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class CreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password, self.instance)
        return password
        # try:
        #     password_validation.validate_password(password, self.instance)
        # except ValidationError as error:
        #     self.add_error()