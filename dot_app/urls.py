from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('boards/', views.Board_ListView.as_view(), name='boards'),
    path('book/', views.board_view, name='board'),
    path('manufacturers/', views.Manufacturer_ListView.as_view(), name='manufacturers'),
    path('manufacturer/', views.manufacturer_view, name='manufacturer'),
    path('subtypes/', views.Subtype_ListView.as_view(), name='subtypes'),
    path('subtype/', views.subtype_view, name='subtype'),
]