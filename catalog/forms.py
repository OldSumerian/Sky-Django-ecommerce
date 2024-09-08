from django import forms

from catalog.models import Product, ProductVersion


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        cleaned_name = self.cleaned_data['name']
        forbidden_words = [
            'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
        ]
        if any(word in cleaned_name.lower() for word in forbidden_words):
            raise forms.ValidationError("Запрещенные слова в названии товара")
        return cleaned_name

    def clean_description(self):
        cleaned_description = self.cleaned_data['description']
        forbidden_words = [
            'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
        ]
        if any(word in cleaned_description.lower() for word in forbidden_words):
            raise forms.ValidationError("Запрещенные слова в описании товара")
        return cleaned_description


class ProductVersionForm(forms.ModelForm):
    class Meta:
        model = ProductVersion
        fields = ('version_number', 'version_name', 'is_current')
        widgets = {
            'version_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'version_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'version_number': 'Номер версии',
            'version_name': 'Название версии',
            'is_current': 'Текущая версия',
        }
        help_texts = {
            'version_number': 'Укажите номер версии продукта.',
            'version_name': 'Укажите название версии продукта.',
            'is_current': 'Укажите признак текущей версии.',
        }

        # def __init__(self):
        #     self.cleaned_data = None
        #
        # def clean_version_number(self):
        #     cleaned_version_number = self.cleaned_data
        #     if cleaned_version_number <= 0:
        #         raise forms.ValidationError("Номер версии должен быть положительным числом.")
        #     return cleaned_version_number
        
class ProductFormFromModerator(forms.ModelForm):


    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published')