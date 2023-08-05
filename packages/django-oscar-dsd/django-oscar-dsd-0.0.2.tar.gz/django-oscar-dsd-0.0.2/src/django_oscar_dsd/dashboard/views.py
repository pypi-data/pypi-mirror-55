from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ungettext, ugettext_lazy as _
from django.views.generic import (
    ListView, DeleteView, CreateView, UpdateView, View)

from oscar.views.generic import BulkEditMixin
from oscar.core.loading import get_classes, get_model

from ..models import DSDProduct
from .forms import DSDProductForm, DSDPublishProductForm


Product = get_model('catalogue', 'Product')


class DSDProductListView(ListView):
    model = DSDProduct
    context_object_name = 'dsd_products'
    template_name = 'dsd/dashboard/dsd_product_list.html'


class DSDProductCreateView(CreateView):
    model = DSDProduct
    template_name = 'dsd/dashboard/dsd_product_form.html'
    form_class = DSDProductForm

    def get_success_url(self):
        messages.success(self.request, _("DSDProduct created"))
        return reverse('dashboard:dsd_product-list')

    def get_context_data(self, **kwargs):
        ctx = super(DSDProductCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Create dsd_product")
        return ctx


class DSDProductUpdateView(UpdateView):
    model = DSDProduct
    template_name = 'dsd/dashboard/dsd_product_form.html'
    form_class = DSDProductForm

    def get_object(self):
        obj = super(DSDProductUpdateView, self).get_object()
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Product updated"))
        return reverse('dashboard:dsd_product-list')

    def get_context_data(self, **kwargs):
        ctx = super(DSDProductUpdateView, self).get_context_data(**kwargs)
        ctx['dsd_product'] = self.object
        ctx['title'] = self.object.name
        return ctx


class DSDProductDeleteView(DeleteView):
    model = DSDProduct
    template_name = 'dsd/dashboard/dsd_product_delete.html'
    context_object_name = 'dsd_product'

    def get_success_url(self):
        messages.success(self.request, _("Product deleted"))
        return reverse('dashboard:dsd_product-list')


class DSDProductPublishView(UpdateView):
    model = DSDProduct
    template_name = 'dsd/dashboard/dsd_product_publish.html'
    context_object_name = 'dsd_product'
    form_class = DSDPublishProductForm

    def get_object(self):
        obj = super(DSDProductPublishView, self).get_object()
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Product published"))
        return reverse('dashboard:dsd_product-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.publish()

        return super(DSDProductPublishView, self).post(request, *args, **kwargs)
