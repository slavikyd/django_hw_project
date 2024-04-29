from typing import Any
from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator

from .models import Board, Subtype, Manufacturer

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
    def view(request):
        id_ = request.GET.get('id', None)
        target = model_class.objects.get(id=id_) if id_ else None
        return render(request, template, {context_name: target})
    return view


Board_ListView = create_list_view(Board, 'boards', 'catalog/boards.html')
Subtype_ListView = create_list_view(Subtype, 'subtypes', 'catalog/subtypes.html')
Manufacturer_ListView = create_list_view(Manufacturer, 'manufacturers', 'catalog/manufacturers.html')

board_view = create_view(Board, 'board', 'entities/board.html')
subtype_view = create_view(Subtype, 'subtype', 'entities/subtype.html')
manufacturer_view = create_view(Manufacturer, 'manufacturer', 'entities/manufacturer.html')

