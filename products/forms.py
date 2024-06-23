from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse_lazy
from .models import Product

class StyleFormMixin:


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):  # Пример для поля типа Select
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'price', 'is_active')
        success_url = reverse_lazy('products:detail_list')

    def clean_name(self):
        name = self.cleaned_data['name']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in forbidden_words:
            if word in name.lower():
                raise forms.ValidationError(f'Название не должно содержать запрещенное слово: {word}')
        return name


    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        self.fields['name'].widget.attrs.update({'placeholder': 'Enter name'})
        self.fields['price'].widget.attrs.update({'placeholder': 'Enter price'})
ProductForm.base_fields['is_active'].widget.attrs['class'] = 'form-check-input'
