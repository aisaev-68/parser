import logging
from django.shortcuts import render
from django.views import View
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
        run_parser()
        return render(request, 'rate/catalog.html')
