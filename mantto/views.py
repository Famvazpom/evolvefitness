from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class indexView(TemplateView):
    template_name = "mantto/index.html"
