from django.urls import path
from .views import RateView


app_name = 'api'
urlpatterns = [
    path('rates/', RateView.as_view(), name="rate_list"),
    path("rate/<int:pk>/", RateView.as_view(), name="rate_by_id"),
]