from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('home/',login_required(views.homeView.as_view()),name='home'),
    path('a/',views.indexView.as_view(),name="index"),
]