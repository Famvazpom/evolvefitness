from django.urls import path
from . import views

urlpatterns = [
    path('',views.landingView.as_view(),name="landing"),
    path('en/',views.landingViewEn.as_view(),name="landing_en"),
]