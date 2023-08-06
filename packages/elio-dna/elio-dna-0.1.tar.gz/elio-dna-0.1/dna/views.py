# -*- encoding: utf-8 -*-
from django.apps import apps
from django.conf import settings
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from dna.dna import DnaOfDjangoModel
from dna.forms import every_form


class EveryViewMixin:
    app_name = None

    @property
    def dna(self):
        return DnaOfDjangoModel(
            settings.SCHEMA_PATH, "chromosomes", elio_list=settings.ELIO_LIST
        ).dna_of_models(list(settings.DNA_THINGS), settings.DNA_DEPTH)

    @property
    def thing_name(self):
        return self.kwargs.get("thing_name", None)

    @property
    def things(self):
        return [
            f"{self.app_name}{t}" for t in sorted(list(settings.DNA_THINGS))
        ]

    @property
    def Model(self):
        if self.thing_name:
            return apps.get_model(
                model_name=self.thing_name, app_label=self.app_name.lower()
            )
        return None

    @property
    def ElioList(self):
        if self.thing_name and settings.ELIO_LIST:
            return apps.get_model(
                model_name="ElioList", app_label=self.app_name.lower()
            )
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["thing_name"] = self.thing_name
        context["things"] = self.things
        return context


class EveryQuerySetMixin:

    paginate_by = 20

    def get_queryset(self):
        return self.Model.objects.all().order_by("name")


class EveryGetObjectMixin:
    def get_object(self):
        obj = self.Model.objects.get(pk=self.kwargs.get("pk"))
        return obj


class EveryEditMixin:
    def get_form_class(self):
        return every_form(self.Model)


class EveryCreateViewMixin(
    EveryViewMixin, EveryGetObjectMixin, EveryEditMixin, CreateView
):
    pass


class EveryDetailViewMixin(
    EveryViewMixin, EveryQuerySetMixin, EveryGetObjectMixin, DetailView
):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["elio_list"] = self.dna[self.thing_name]["list_fields"]
        if settings.ELIO_LIST:
            context["list"] = self.ElioList.objects.filter(
                parent_model=self.get_object()
            )
        return context


class EveryDeleteViewMixin(
    EveryViewMixin, EveryGetObjectMixin, EveryQuerySetMixin, DeleteView
):
    success_url = reverse_lazy("things")


class ElioListCreateViewMixin(EveryCreateViewMixin):
    def get_form_class(self):
        field_name = self.kwargs.get("field_name")
        field_dna = self.dna[self.thing_name]["list_fields"][field_name]
        ListModel = apps.get_model(
            model_name=field_dna["related_to"], app_label=self.app_name.lower()
        )
        return every_form(ListModel)


class EveryUpdateViewMixin(
    EveryViewMixin, EveryGetObjectMixin, EveryEditMixin, UpdateView
):
    pass


class EveryListViewMixin(EveryViewMixin, EveryQuerySetMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["thing_parent"] = self.kwargs.get("thing_parent", "App")
        return context
