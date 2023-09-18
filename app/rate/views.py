import logging
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

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
        # Показать страницу с сообщением о начале парсинга
        return render(request, 'rate/progress_parser.html')
