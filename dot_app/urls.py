from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet, SubtypeViewSet, ManufacturerViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

router = DefaultRouter()
router.register(r'boards', BoardViewSet)
router.register(r'subtypes', SubtypeViewSet)
router.register(r'manufacturers', ManufacturerViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v0.1',
      description="Empty now",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="a@a.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls), name='api'),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
    path('boards/', views.Board_ListView.as_view(), name='boards'),
    path('board/', views.board_view, name='board'),
    path('manufacturers/', views.Manufacturer_ListView.as_view(), name='manufacturers'),
    path('manufacturer/', views.manufacturer_view, name='manufacturer'),
    path('register/', views.register, name='register'),
    path('subtypes/', views.Subtype_ListView.as_view(), name='subtypes'),
    path('subtype/', views.subtype_view, name='subtype'),
    path('test_form/', views.test_form, name='test_form'),
    path('dot_swagger/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('404/', views.not_found_page, name='404_page'),
    path('profile/', views.profile, name='profile')
]
urlpatterns += staticfiles_urlpatterns()
