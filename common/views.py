from django.shortcuts import redirect
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


class DocumentationView(TemplateView):
    template_name = 'documentation.html'


def redirect_home(request):
    return redirect('home')
