from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.urls import path, include


urlpatterns = [
    # path('', TemplateView.as_view(template_name="rate/catalog.html"), name='index'),
    path('', include('rate.urls')),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


