"""Urls routing module for django project."""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('boards', views.BoardViewSet)
router.register('subtypes', views.SubtypeViewSet)
router.register('manufacturers', views.ManufacturerViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title='Snippets API',
      default_version='v0.1',
      description='Empty now',
      terms_of_service='https://www.google.com/policies/terms/',
      contact=openapi.Contact(email='slavikyd@gmail.com'),
      license=openapi.License(name='BSD License'),
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
   path('profile/', views.profile, name='profile'),
   path('bookmark/', views.bookmark, name='bookmark'),
   path('search/', views.search_feature, name='search'),
   path('about/', views.about_page, name='about'),
   path('tutorials/', views.Tutorials_ListView.as_view(), name='tutorials'),
]
urlpatterns += staticfiles_urlpatterns()
