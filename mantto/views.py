from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class BaseView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = 'Mantenimiento'
        return context

class homeView(BaseView):
    template_name = 'mantto/main_menu.html'


class indexView(BaseView):
    template_name = "mantto/index.html"


