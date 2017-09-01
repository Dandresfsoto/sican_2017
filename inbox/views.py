from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
# Create your views here.

class Inbox(LoginRequiredMixin,TemplateView):
    template_name = "inbox/inicio.html"