"""Views module for django project."""
from typing import Any

from django.contrib.auth import decorators, logout, mixins
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic import ListView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

from .forms import Registration, TestForm
from .models import Board, BoardBoard, Client, Manufacturer, Subtype
from .serializers import BoardSerializer, ManufacturerSerializer, SubtypeSerializer

POST_STR = 'POST'
BOARDS = 'boards'


def home_page(request):
    """Webpage view creation attribute.

    Args:
        request (_type_): request from user

    Returns:
        render: rendered html page.
    """
    return render(
        request,
        'index.html',
        {
            BOARDS: Board.objects.count(),
            'subtypes': Subtype.objects.count(),
            'manufacturers': Manufacturer.objects.count(),
        },
    )


def not_found_page(request):
    """404 not found webpage view.

    Args:
        request (_type_): request from user

    Returns:
        render: error page
    """
    return render(request, '404.html')


def create_list_view(model_class, plural_name, template):
    """Class assemblying func for listviewset.

    Args:
        model_class (_type_): class of model that we are using
        plural_name (_type_): plural name for the model
        template (_type_): html template for viewset

    Returns:
        ModelListView: class that can be rendered to webpage with list view of models.
    """
    class ModelListView(mixins.LoginRequiredMixin, ListView):
        """Custom ListView class.

        Args:
            LoginRequiredMixin (_type_): Mixin from django as alternative for @login_required
            ListView (_type_): django base ListView inheritance

        Returns:
            context: dict for template render
        """

        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            """_summary_.

            Args:
                kwargs: just plain steal of them for attribute proper work

            Returns:
                dict[str, Any]: _description_
            """
            context = super().get_context_data(**kwargs)
            obj = model_class.objects.all()
            paginator = Paginator(obj, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context
    return ModelListView


Board_ListView = create_list_view(Board, BOARDS, 'catalog/boards.html')
Manufacturer_ListView = create_list_view(
    Manufacturer,
    'manufacturers',
    'catalog/manufacturers.html',
)
Subtype_ListView = create_list_view(Subtype, 'subtypes', 'catalog/subtypes.html')


def create_view(model_class, context_name, template):
    """View assembler for single record of some model.

    Args:
        model_class (_type_): model class
        context_name (_type_): name of the model
        template (_type_): html template for page render

    Returns:
        view: function that renders html page
    """
    @decorators.login_required
    def view(request):
        """View assember.

        Args:
            request (_type_): user request

        Returns:
            render: rendered web page
        """
        id_ = request.GET.get('id', None)
        target = model_class.objects.get(id=id_) if id_ else None
        context = {context_name: target}
        if model_class == Board:
            client = Client.objects.get(user=request.user)
            context['client_bookmarked_board'] = target in client.boards.all()
            boards = BoardBoard.objects.filter(theboard__id=id_)
            context['compatible_boards'] = boards
        return render(
            request,
            template,
            context,
        )
    return view


def test_form(request):
    """Test form view.

    Args:
        request (_type_): user request.

    Returns:
        _type_: rendered form
    """
    context = {'form': TestForm()}
    for key in ('text', 'number', 'choice'):
        context[key] = request.GET.get(key, f'{key} was not provided!')
    return render(
        request,
        'pages/test_form.html',
        context,
    )


def register(request):
    """User registration attribute.

    Args:
        request (_type_): user request

    Returns:
        _type_: form of registration or errors if something went wrong.
    """
    errors = ''
    if request.method == POST_STR:
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
        },
    )


class MyPermission(BasePermission):
    """Custom BasePermission class.

    Args:
        BasePermission (_type_): base inheritance

    """

    _safe_methods = 'GET', 'HEAD', 'OPTIONS', 'PATCH'
    _unsafe_methods = POST_STR, 'PUT', 'DELETE'

    def has_permission(self, request, _):
        """Permission checker for Permission class.

        Args:
            request (_type_): user request
            _ (_type_): blank arg

        Returns:
            bool: allowing or not allowing user to do some of the requests
        """
        if request.method in self._safe_methods and (request.user and request.user.is_authenticated):
            return True
        if request.method in self._unsafe_methods and (request.user and request.user.is_superuser):
            return True
        return False


def create_viewset(model_class, serializer):
    """Viewset class assemblying attribute.

    Args:
        model_class (_type_): class of model
        serializer (_type_): serializer class

    Returns:
        CustomViewSet: ViewSet for REST usage
    """
    class CustomViewSet(ModelViewSet):
        """ViewSet for REST implementation.

        Args:
            ModelViewSet (_type_): base REST framework inheritance
        """

        serializer_class = serializer
        queryset = model_class.objects.all()
        permission_classes = [MyPermission]
        authentication_classes = [TokenAuthentication]

    return CustomViewSet


@decorators.login_required
def profile(request):
    """Profile page assemblying func.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    client = Client.objects.get(user=request.user)

    client_attrs = 'username', 'first_name', 'last_name'
    client_data = {attr: getattr(client, attr) for attr in client_attrs}
    return render(
        request,
        'pages/profile.html',
        {
            'client_data': client_data,
            'client_boards': client.boards.all(),
        },
    )


@decorators.login_required
def bookmark(request):
    """Bookmark method for boards.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    client = Client.objects.get(user=request.user)
    id_ = request.GET.get('id', None)
    if not id_:
        return redirect(BOARDS)
    try:
        board = Board.objects.get(id=id_)
    except (ValidationError, ObjectDoesNotExist):
        return redirect(BOARDS)
    if not board:
        return redirect(BOARDS)
    if board in client.boards.all():
        return redirect('profile')

    if request.method == POST_STR:
        client.boards.add(board)
        client.save()
        return redirect('profile')

    return render(
        request,
        'pages/bookmark.html',
        {
            'board': board,
        },
    )


@decorators.login_required
def user_logout(request):
    """User logging out attribute.

    Args:
        request (_type_): user request

    Returns:
        render: logged out html template
    """
    logout(request)
    return render(request, 'registration/logged_out.html', {})


def search_feature(request):
    """Search feature for Board model.

    Args:
        request (_type_): user request

    Returns:
        _type_: search_page template
    """
    if request.method == POST_STR:
        search_query = request.POST['search_query']
        posts = Board.objects.filter(title__contains=search_query)
        return render(request, 'pages/search_page.html', {'query': search_query, 'posts': posts})
    return render(request, 'pages/search_page.html', {})


Board_ListView = create_list_view(Board, BOARDS, 'catalog/boards.html')
Subtype_ListView = create_list_view(Subtype, 'subtypes', 'catalog/subtypes.html')
Manufacturer_ListView = create_list_view(Manufacturer, 'manufacturers', 'catalog/manufacturers.html')

board_view = create_view(Board, 'board', 'entities/board.html')
subtype_view = create_view(Subtype, 'subtype', 'entities/subtype.html')
manufacturer_view = create_view(Manufacturer, 'manufacturer', 'entities/manufacturer.html')


BoardViewSet = create_viewset(Board, BoardSerializer)
SubtypeViewSet = create_viewset(Subtype, SubtypeSerializer)
ManufacturerViewSet = create_viewset(Manufacturer, ManufacturerSerializer)
