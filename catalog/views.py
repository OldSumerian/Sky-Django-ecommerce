from itertools import product
from pathlib import Path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from catalog.forms import ProductForm, ProductVersionForm, ProductFormFromModerator
from catalog.services import get_products_from_cache, get_categories_from_cache
from config import settings
from catalog.models import Product, ProductVersion, Category

FEEDBACK_FILE_PATH: Path = settings.BASE_DIR.joinpath("feedback.json")

class CategoryListView(ListView):
    model = Category

    def get_queryset(self):
        return get_categories_from_cache()

class CatalogListView(ListView):
    model = Product

    def get_queryset(self):
        return get_products_from_cache()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        for prod in context_data['object_list']:
            versions = prod.product_versions.get_queryset()
            if not versions:
                prod.current_version = 'Версия не указана'
            else:
                active_version = versions.filter(is_current=True).first()
                if active_version is None:
                    prod.current_version = 'Версия не выбрана'
                else:
                    prod.current_version = active_version.version_name
        return context_data


class CatalogDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class CatalogCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")


    def form_valid(self, form):
        product = form.save()
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)



class CatalogUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_form_class(self):
        if self.request.user.is_superuser or self.request.user == self.object.owner:
            return super().get_form_class()
        elif self.request.user.has_perms(
                [
                    'catalog.published_rights',
                    'catalog.description_rights',
                    'catalog.category_rights'
                ]
        ):
            return ProductFormFromModerator
        else:
            raise PermissionDenied("У вас недостаточно прав для редактирования этого товара")

    def get_success_url(self):
        return reverse(viewname="catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user == self.object.owner:
            ProductVersionFormset = inlineformset_factory(Product, ProductVersion, ProductVersionForm, extra=1)
            if self.request.method == "POST":
                context_data["formset"] = ProductVersionFormset(self.request.POST, instance=self.object)
            else:
                context_data["formset"] = ProductVersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        if 'formset' in context_data:
            formset = context_data['formset']
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form, formset=formset))
        else:
            return super().form_valid(form)


class CatalogDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"
    context_object_name = "contacts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["contacts"] = json.loads(FEEDBACK_FILE_PATH.read_text(encoding='utf-8'))
        return context
