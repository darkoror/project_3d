from django.contrib.auth import views
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.template.response import SimpleTemplateResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView

from authentication import tasks
from authentication.forms import CustomAuthenticationForm, RegisterForm, ActivateAccountForm
from common.utils import build_url
from project_3d.settings import ACTIVATION_PATH


class CustomLoginView(views.LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm


class CustomLogoutView(views.LogoutView):
    template_name = 'registration/logout.html'


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            context = {
                'link': build_url(
                    scheme=self.request.scheme,
                    uid=urlsafe_base64_encode(force_bytes(user.id)),
                    token=default_token_generator.make_token(user),
                    path=ACTIVATION_PATH
                )
            }
            tasks.send_email.delay(
                subject="email/activate_account_subject.txt",
                template="email/activate_account.html",
                recipients=[user.email], context=context
            )
            return SimpleTemplateResponse('registration/success_register.html', status=201)

        return render(request, self.template_name, context={'form': form}, status=400)


class ActivateAccountView(FormView):
    template_name = 'registration/activate_account.html'
    form_class = ActivateAccountForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['token'] = self.request.GET.get('token')
        return kwargs

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        if form.is_valid():
            form.activate_user()
            return SimpleTemplateResponse(self.template_name, context={'form': form}, status=200)

        return SimpleTemplateResponse(self.template_name, context={'form': form}, status=400)
