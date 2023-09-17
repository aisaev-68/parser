import logging
from django.shortcuts import render
from django.views import View
from rest_framework.pagination import PageNumberPagination

from .models import Rate
from .serializers import RateSerializer
from .parser import run_parser

logger = logging.getLogger(__name__)

class MainPageView(View):
    """
    Представление для перехода на главную страницу.
    """

    def get(self, request, *args, **kwargs):
        logger.info('Переход на главную страницу')
        return render(request, 'rate/catalog.html')


class ParseUpdate(View):

    def get(self, request, *args, **kwargs):
        run_parser()  # Запуск парсинга и обновления данных
        return render(request, 'rate/catalog.html')
