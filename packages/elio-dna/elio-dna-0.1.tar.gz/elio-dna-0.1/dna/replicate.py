"""ReplicateDjangoModel: Return django models.

This class builds a dynamic django models from any list of schema.org "Things".


**Usage**

::

    from dna.dna import DnaOfDjangoModel
    from dna.replicate import ReplicateDjangoModel

    dna_maker = DnaOfDjangoModel("schema.jsonld", "app")
    dna = dna_maker.dna_of_models(["Thing"], 1)
    replicator = ReplicateDjangoModel(dna, "app")
    replicator.start_replication()"""
# -*- encoding: utf-8 -*
from django.db import models
from django.conf import settings
from django.urls import reverse
from polymorphic.models import PolymorphicModel


def every_model(dna, model_app_label):
    """Utility function to build every model + the eliolist model."""
    replicator = ReplicateDjangoModel(dna, model_app_label)
    replicator.start_replication()


def eliolist_model(model_app_label):
    class ElioList(models.Model):
        parent_model = models.ForeignKey(
            f"{model_app_label.title()}Thing",
            on_delete=models.CASCADE,
            related_name="parent_to_list",
        )
        listed_model = models.ForeignKey(
            f"{model_app_label.title()}Thing",
            on_delete=models.CASCADE,
            related_name="listed_by_parent",
        )
        field_name = models.CharField(max_length=100)

        class Meta:
            app_label = model_app_label
            unique_together = ["parent_model", "listed_model", "field_name"]

    return ElioList


class ReplicateDjangoModel:
    """Build django models from the DNA."""

    def __init__(self, model_dna, model_app_label):
        # Schema.org jsonld information as parsable units.
        self.dna = model_dna
        # The django app_label for the target django app.
        self.app_label = model_app_label
        # Holding places for the structure `ReplicateDjangoModel` builds.
        self.models_loaded = {"models.Model": PolymorphicModel}

    def get_model_field_dynamically(self, dna_of_field):
        """Returns an instance of a django model type."""
        field_type = dna_of_field.pop("field_type")
        if field_type == "ForeignKey":
            related_to = dna_of_field.pop("related_to")
            dna_of_field["on_delete"] = models.CASCADE
            return models.ForeignKey(related_to, **dna_of_field)
        else:
            django_model_type = getattr(models, field_type)
            return django_model_type(**dna_of_field)

    def get_model_inheritance(self, inherit_from):
        """Get or create a model required for inheritance."""
        model_inheritance = self.models_loaded.get(inherit_from, None)
        if not model_inheritance:
            model_inheritance = self.replicate_django_model(
                inherit_from, self.dna[inherit_from]
            )
        return model_inheritance

    def replicate_django_model(
        self, app_model_name, dna_of_model, options=None
    ):
        """Return a django model given a class object.

        :param dna_of_model: e.g.
            {
                "fields_of": {
                    "name": {
                        "field_type": "CharField",
                        "max_length": 512,
                        "blank": true,
                    },
                    "identifier": {
                        "blank": true,
                        "field_type": "ForeignKey",
                        "related_name": "dnathing_dnacreativework_about",
                        "related_to": "Thing",
                        "null": true,
                    },
                    "description": {"field_type": "TextField", "blank": true},
                },
                "inherits_from": ["base.Model"],
                "model_name": "AppnameThing",
            }
        """
        # Don't keep getting the same model over and over.
        model = self.models_loaded.get(app_model_name, None)
        if model:
            return model

        class Meta:
            db_table = f"{app_model_name}"
            app_label = self.app_label

        def get_absolute_url(self):
            return reverse(
                "engage.thing", args=[f"{app_model_name}", str(self.pk)]
            )

        def get_fields(self):
            return [
                (field.name, type(field).__name__, getattr(self, field.name))
                for field in self._meta.fields
                if type(field).__name__ not in ["ImageField", "FileField"]
            ]

        def get_images(self):
            return [
                (
                    field.name,
                    self.image.url,
                    self.image.height,
                    self.image.width,
                )
                for field in self._meta.fields
                if self.image and type(field).__name__ in ["ImageField"]
            ]

        def __str__(self):
            return self.name

        # Update Meta with any options that were provided
        if options is not None:
            for key, value in options.iteritems():
                setattr(Meta, key, value)

        # Set up a dictionary to simulate declarations within a class
        attrs = {
            "__module__": __name__,
            "__str__": __str__,
            "Meta": Meta,
            "get_absolute_url": get_absolute_url,
            "get_fields": get_fields,
            "get_images": get_images,
        }
        # Model Inheritance.
        inheritance = []
        for inherit_from in dna_of_model["inherits_from"]:
            model_inheritance = self.get_model_inheritance(inherit_from)
            inheritance.append(model_inheritance)

        # Fields.
        for field_name, dna_of_field in dna_of_model["fields_of"].items():
            attrs[field_name] = self.get_model_field_dynamically(dna_of_field)
        # Manually create the inheritance pointer.
        for point_to in inheritance:
            if not point_to.__name__ == "PolymorphicModel":
                attrs[
                    f"{app_model_name}_to_{point_to.__name__}".lower()
                ] = models.OneToOneField(
                    f"{point_to.__name__}",
                    parent_link=True,
                    on_delete=models.CASCADE,
                )
        # Create the class, which automatically triggers ModelBase processing.
        model = type(f"{app_model_name}", tuple(inheritance), attrs)
        # Store it so that we can pick it up for inheritance.
        self.models_loaded[app_model_name] = model
        # Return the model.
        return model

    def start_replication(self):
        """Build all the models."""
        # Do each model in any order
        for app_model_name, model_dna in self.dna.items():
            self.replicate_django_model(app_model_name, model_dna)
