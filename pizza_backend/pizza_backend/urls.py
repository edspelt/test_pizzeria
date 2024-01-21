from django.contrib import admin
from django.urls import path, include, re_path, reverse_lazy
from django.views.generic.base import RedirectView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from drf_yasg.generators import OpenAPISchemaGenerator

class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_security_definitions(self):
        return {
            'Token': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        }

schema_view = get_schema_view(
    openapi.Info(
        title="Pizza API",
        default_version='v1',
        description="API test para pizzeria",
    ),
    public=True,
    permission_classes=(AllowAny,),
    generator_class=CustomSchemaGenerator,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pizza_app.urls')),
    re_path(r'^swagger(?P<format>\\.json|\\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', RedirectView.as_view(url=reverse_lazy('schema-swagger-ui'), permanent=False)),  # Redirección a Swagger
]
