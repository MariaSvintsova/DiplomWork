from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from rest_framework import request

from products.forms import ProductForm
from django.views.decorators.vary import vary_on_cookie
from products.models import Product
from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    pagination_class = ProductPagination
    paginate_by = 4


    def get_queryset(self):
        queryset = Product.objects.all()
        paginator = self.pagination_class()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Context object_list count:", len(context['object_list']))  # Отладочный вывод
        products = Product.objects.all()
        context['object_list'] = products
        return context

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data

    def form_valid(self, form):
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products:home')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("У вас нет прав на редактирование этого товара.")
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


@cache_page(60)
def toggle_activity(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    product_item.is_active = not product_item.is_active
    product_item.save()
    return redirect(reverse('products:home'))

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products:home')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("У вас нет прав на удаление этого товара.")
        return super().handle_no_permission()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if hasattr(self.object, 'owner') and self.request.user == self.object.owner:
            return super().delete(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("У вас нет прав на удаление этого товара.")
