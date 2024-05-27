from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status


from .models import Board, Subtype, Manufacturer, Client
from .forms import TestForm, Registration
from .serializers import BoardSerializer, SubtypeSerializer, ManufacturerSerializer

def home_page(request):
    return render(
        request,
        'index.html',
        {
            'boards': Board.objects.count(),
            'subtypes': Subtype.objects.count(),
            'manufacturers': Manufacturer.objects.count(),
        }
    )

def not_found_page(request):
    return render(request, '404.html')

def create_list_view(model_class, plural_name, template):
    class ModelListView(ListView):
        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            obj = model_class.objects.all()
            paginator = Paginator(obj, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context
    return ModelListView

Board_ListView = create_list_view(Board, 'boards', 'catalog/boards.html')
Manufacturer_ListView = create_list_view(Manufacturer, 'manufacturers', 'catalog/manufacturers.html')
Subtype_ListView = create_list_view(Subtype, 'subtypes', 'catalog/subtypes.html')

def create_view(model_class, context_name, template):
    @login_required
    def view(request):
        id_ = request.GET.get('id', None)
        target = model_class.objects.get(id=id_) if id_ else None
        context = {context_name: target}
        return render(
            request,
            template,
            context,
        )
    return view


def test_form(request):
    context = {'form': TestForm()}
    for key in ('text', 'number', 'choice'):
        context[key] = request.GET.get(key, f'{key} was not provided!')
    return render(
        request,
        'pages/test_form.html',
        context,
    )

def register(request):
    errors = ''
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
        else:
            errors = form.errors
    else:
        form = Registration()

    return render(
        request,
        'registration/register.html',
        {
            'form': form,
            'errors': errors,
        }
    )

class MyPermission(BasePermission):
    _safe_methods = 'GET', 'HEAD', 'OPTIONS', 'PATCH'
    _unsafe_methods = 'POST', 'PUT', 'DELETE'

    def has_permission(self, request, _):
        if request.method in self._safe_methods and (request.user and request.user.is_authenticated):
            return True
        if request.method in self._unsafe_methods and (request.user and request.user.is_superuser):
            return True
        return False

def create_viewset(model_class, serializer):
    class CustomViewSet(ModelViewSet):
        serializer_class = serializer
        queryset = model_class.objects.all()
        permission_classes = [MyPermission]
        authentication_classes = [TokenAuthentication]

    return CustomViewSet

@login_required
def profile(request):
    client = Client.objects.get(user=request.user)

    
    client_attrs = 'username', 'first_name', 'last_name'
    client_data = {attr: getattr(client, attr) for attr in client_attrs}
    return render(
        request,
        'pages/profile.html',
        {
            'client_data': client_data,
            'client_boards': client.boards.all(),
        }
    )

@login_required
def bookmark(request):
    client = Client.objects.get(user=request.user)
    id_ = request.GET.get('id', None)
    if not id_:
        return redirect('boards')
    try:
        board = Board.objects.get(id=id_)
    except (ValidationError, ObjectDoesNotExist):
        return redirect('boards')
    if not board:
        return redirect('boards')
    if board in client.boards.all():
        return redirect('profile')



    return render(
        request,
        'pages/bookmark.html',
        {
            'board': board,
        }
    )


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html', {})

Board_ListView = create_list_view(Board, 'boards', 'catalog/boards.html')
Subtype_ListView = create_list_view(Subtype, 'subtypes', 'catalog/subtypes.html')
Manufacturer_ListView = create_list_view(Manufacturer, 'manufacturers', 'catalog/manufacturers.html')

board_view = create_view(Board, 'board', 'entities/board.html')
subtype_view = create_view(Subtype, 'subtype', 'entities/subtype.html')
manufacturer_view = create_view(Manufacturer, 'manufacturer', 'entities/manufacturer.html')


BoardViewSet = create_viewset(Board, BoardSerializer)
SubtypeViewSet = create_viewset(Subtype, SubtypeSerializer)
ManufacturerViewSet = create_viewset(Manufacturer, ManufacturerSerializer)