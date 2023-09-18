from django.urls import path
from .views import RateView, UpdateRateView


app_name = 'api'
urlpatterns = [
    path('rates/', RateView.as_view(), name="rate_list"),
    path("update/", UpdateRateView.as_view(), name="update_rate"),
]