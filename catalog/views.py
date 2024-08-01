from pathlib import Path

from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from catalog.forms import ProductForm, ProductVersionForm
from config import settings
from catalog.models import Product, ProductVersion

FEEDBACK_FILE_PATH: Path = settings.BASE_DIR.joinpath("feedback.json")


class CatalogListView(ListView):
    model = Product

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


class CatalogCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")


class CatalogUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_success_url(self):
        return reverse(viewname="catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductVersionFormset = inlineformset_factory(Product, ProductVersion, ProductVersionForm, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = ProductVersionFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = ProductVersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class CatalogDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"
    context_object_name = "contacts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["contacts"] = json.loads(FEEDBACK_FILE_PATH.read_text(encoding='utf-8'))
        return context
