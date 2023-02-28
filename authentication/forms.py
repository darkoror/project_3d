from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.forms import EmailField, Form
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from authentication.models import User


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(email=username)
                except BaseException:
                    user_temp = None

                if user_temp is not None:
                    self.confirm_login_allowed(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )

        return self.cleaned_data


class ActivateAccountForm(Form):
    token = forms.CharField(required=True)

    def clean(self):
        data = self.cleaned_data
        try:
            uid, token = data['token'].split('.')
            user_id = int(force_str(urlsafe_base64_decode(uid)))
        except (TypeError, ValueError):
            raise forms.ValidationError({'token': 'invalid token'})

        try:
            self.user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise forms.ValidationError({'token': 'invalid token'})

        if not default_token_generator.check_token(self.user, token):
            raise forms.ValidationError({'token': 'invalid token'})

        return data

    def activate_user(self):
        """if token is valid then activate the user, after that user can log in"""
        self.user.is_active = True
        self.user.save()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)
        field_classes = {'email': EmailField}

    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()
