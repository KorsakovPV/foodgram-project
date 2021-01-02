from django import forms
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()


class CreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            auth_user = authenticate(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password']
            )
            login(self.request, auth_user)
        return user


