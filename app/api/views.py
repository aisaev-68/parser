import logging
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from rate.models import Rate
from rate.serializers import RateSerializer
from rate.parser import run_parser

logger = logging.getLogger(__name__)


class RateView(APIView):
    """
    Представление для фильтрации услуг по характеристикам и сортировки услуг.
    """
    template_name = 'rate/catalog.html'

    def filter_queryset(self, queryset):
        # Извлечение параметров запроса
        sort = self.request.query_params.get('sort')
        sort_type = self.request.query_params.get('sortType')
        name_filter = self.request.query_params.get('filter[name]')
        min_price = self.request.query_params.get('filter[minPrice]')
        max_price = self.request.query_params.get('filter[maxPrice]')

        if name_filter:
            queryset = queryset.filter(card_title__icontains=name_filter)
        if min_price:
            queryset = queryset.filter(price_main__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_main__lte=max_price)

        if sort:
            sort_field = '-' + sort if sort_type == 'dec' else sort
            queryset = queryset.order_by(sort_field)

        return queryset

    def pagination_queryset(self, queryset):
        len_products = len(queryset)
        paginator = PageNumberPagination()
        limit = 6

        paginator.page_size = limit
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        current_page = int(self.request.GET.get('page', 1))
        if len_products % limit == 0:
            last_page = len_products // limit
        else:
            last_page = len_products // limit + 1

        return {
            'pagination': paginated_queryset,
            'currentPage': current_page,
            'lastPage': last_page,
        }

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Rate.objects.all())

        data = self.pagination_queryset(queryset)
        paginated_queryset = data['pagination']
        serialized_data = RateSerializer(paginated_queryset, many=True).data

        response_data = {
            'items': serialized_data,
            'currentPage': data['currentPage'],
            'lastPage': data['lastPage'],
        }

        logger.info("Получаем все тарифы")
        return Response(response_data, status=200)


class UpdateRateView(APIView):

    def post(self, request, *args, **kwargs):
        logger.info("Обновляем данные")
        run_parser()

        return Response({'message': 'Данные успешно обновлены'}, status=200)
