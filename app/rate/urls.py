from django.urls import path
from .views import MainPageView, ParseUpdate


app_name = 'rate'
urlpatterns = [
    path('', MainPageView.as_view(), name="rate_list"),
    path('parse_update/', ParseUpdate.as_view(), name="parser_update"),
]