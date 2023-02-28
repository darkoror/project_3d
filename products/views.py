from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectTemplateResponseMixin, BaseListView

from products.filters import BundleFilter
from products.forms import ProductCreateForm, ProductUpdateForm, BundleUpdateForm, BundleCreateForm
from products.models import Bundle, Product


class BundleListView(LoginRequiredMixin, MultipleObjectTemplateResponseMixin, BaseListView):
    """Get list of bundles"""
    model = Bundle
    filterset_class = BundleFilter
    template_name = 'products/bundle_list.html'
    success_url = reverse_lazy('products:bundle-list')

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context


class BundleCreateView(LoginRequiredMixin, CreateView):
    form_class = BundleCreateForm
    template_name = 'products/bundle_create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            {'user': request.user}, request.POST
        )
        if form.is_valid():
            product = form.save()
            messages.success(self.request, f'Bundle "{product.name}" was successfully created')
            return HttpResponseRedirect(reverse('products:bundle-list'))

        return render(request, self.template_name, {'form': form})


class BundleDetailView(LoginRequiredMixin, DetailView):
    """Get specific bundle"""
    model = Bundle
    template_name = 'products/bundle_detail.html'
    context_object_name = 'bundle'
    success_url = reverse_lazy('products:bundle-detail')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['bundle_id'], user=self.request.user)


class BundleUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BundleUpdateForm
    template_name = 'products/bundle_update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Bundle, pk=self.kwargs['bundle_id'], user=self.request.user)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        form = self.form_class(instance=product)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        bundle = self.get_object()
        form = self.form_class(
            {'user': request.user}, request.POST, request.FILES, instance=bundle
        )
        if form.is_valid():
            bundle = form.save()
            messages.success(self.request, f'Bundle "{bundle.name}" was successfully updated')
            return HttpResponseRedirect(reverse('products:bundle-detail', args=(bundle.id,)))

        return render(request, self.template_name, {'form': form})


class BundleDeleteView(LoginRequiredMixin, DeleteView):

    def get_object(self, queryset=None):
        return get_object_or_404(Bundle, pk=self.kwargs['bundle_id'], user=self.request.user)

    def post(self, request, *args, **kwargs):
        bundle = self.get_object()
        bundle.delete()
        messages.success(self.request, f'Object "{bundle.name}" was deleted')
        return HttpResponseRedirect(reverse('products:bundle-list'))


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    success_url = reverse_lazy('products:product-detail')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['product_id'], bundle__user=self.request.user)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'product': self.get_object()})


class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductCreateForm
    template_name = 'products/product_create.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Bundle, pk=self.kwargs['bundle_id'], user=self.request.user)

    def get(self, request, *args, **kwargs):
        bundle = self.get_object()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'bundle': bundle})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            {'bundle_id': kwargs.get('bundle_id'), 'user': request.user}, request.POST, request.FILES
        )
        if form.is_valid():
            product = form.save()
            messages.success(self.request, f'Successfully created "{product.name}"')
            return HttpResponseRedirect(reverse('products:bundle-detail', args=(kwargs.get('bundle_id'),)))

        return render(request, self.template_name, {'form': form})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProductUpdateForm
    template_name = 'products/product_update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, pk=self.kwargs['product_id'], bundle__user=self.request.user)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        form = self.form_class(instance=product)
        return render(request, self.template_name, {'form': form, 'bundle': product.bundle})

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = self.form_class(
            {'user': request.user}, request.POST, request.FILES, instance=product
        )
        if form.is_valid():
            product = form.save()
            messages.success(self.request, f'Object "{product.name}" was successfully updated')
            return HttpResponseRedirect(reverse('products:bundle-detail', args=(product.bundle.id,)))

        return render(request, self.template_name, {'form': form})


class ProductDeleteView(LoginRequiredMixin, DeleteView):

    def get_object(self, queryset=None):
        return get_object_or_404(Product, pk=self.kwargs['product_id'], bundle__user=self.request.user)

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        messages.success(self.request, f'Object "{product.name}" was deleted')
        return HttpResponseRedirect(reverse('products:bundle-detail', args=(product.bundle.id,)))
