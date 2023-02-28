from django import forms

from products.models import Product, Bundle


class ProductCreateForm(forms.ModelForm):

    def __init__(self, my_context=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = my_context

    class Meta:
        model = Product
        fields = ('name', 'image', 'asset')

    def clean(self):
        bundle = Bundle.objects.filter(id=self.context['bundle_id'], user=self.context['user']).first()
        if bundle is None:
            raise forms.ValidationError(f"Bundle {self.context['bundle_id']} does not belong you!")
        return {**self.cleaned_data, 'bundle': bundle}

    def save(self, commit=True):
        self.instance.bundle = self.cleaned_data['bundle']
        return super(ProductCreateForm, self).save()


class ProductUpdateForm(forms.ModelForm):

    def __init__(self, my_context=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = my_context

    class Meta:
        model = Product
        fields = ('name', 'image', 'asset')

    def clean(self):
        product = Product.objects.filter(id=self.instance.id, bundle__user=self.context['user']).first()
        if product is None:
            raise forms.ValidationError(f"Product does not belong you!")
        return self.cleaned_data


class BundleCreateForm(forms.ModelForm):

    def __init__(self, my_context=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = my_context

    class Meta:
        model = Bundle
        fields = ('name',)

    def save(self, commit=True):
        self.instance.user = self.context['user']
        return super(BundleCreateForm, self).save()


class BundleUpdateForm(forms.ModelForm):

    def __init__(self, my_context=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = my_context

    class Meta:
        model = Bundle
        fields = ('name',)

    def clean(self):
        bundle = Bundle.objects.filter(id=self.instance.id, user=self.context['user']).first()
        if bundle is None:
            raise forms.ValidationError(f"Bundle does not belong you!")
        return self.cleaned_data
