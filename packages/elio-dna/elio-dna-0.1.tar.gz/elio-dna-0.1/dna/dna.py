"""DnaOfDjangoModel: Return the DNA of django models.

This class builds a dynamic django model from any list of schema.org "Things".


**Usage**

::

    from dna.dna import DnaOfDjangoModel

    dna = DnaOfDjangoModel("schema.jsonld", "app")
    dna.dna_of_models(["Thing"], 1)"""
# -*- encoding: utf-8 -*
import hashlib
from django.apps import apps
from django.db import models
from django.conf import settings
from django.urls import reverse
from dna.crispr import Crispr
from apep.picklejar import PickleJar


class DnaOfDjangoModel:
    """Build the DNA of django models from the Crispr."""

    def __init__(
        self,
        schema_path,
        model_app_label,
        domain="http://schema.org",
        elio_list=False,
        no_comments=False,
    ):
        # Convert schema.org jsonld information into parsable units.
        self.crispr = Crispr(schema_path)
        # The django app_label for the target django app.
        self.app_label = model_app_label
        # Remove comments from the build.
        self.no_comments = no_comments
        # Convert ForeignKeys into many to many elio_lists.
        self.elio_list = elio_list
        # Holding places for the structure `DnaOfDjangoModel` builds.
        self.dna_loaded = {}
        self.class_backbone = []

    @property
    def domain(self):
        # The schema domain.
        return self.crispr.domain

    @staticmethod
    def dna_of_model_field_type_selector(first_type_in, this_list):
        """Gets the first type which matches the list."""
        for type in first_type_in:
            if type in this_list:
                return type
        return None

    def picklings_name(self, thing_names, type_depth):
        shable = "-".join(
            sorted(
                thing_names
                + [str(type_depth), str(self.elio_list), str(self.no_comments)]
            )
        )
        return hashlib.sha1(shable.encode()).hexdigest()[:40]

    def dna_of_model_field_type(self, app_model_name, prp):
        """Selects the best django field Type for any property.

        This works on a sliding scale: Taking the first Type which matches if
        the Property has many.

        1. Use the property_name against predefined lists.
        2. Use the Property Enumerated if Enumerated Type is in dependencies.
        3. Use a Class Type if the Class Type is already in dependencies.
        4. Use the first Django Field for Primitive or semi-Primitive.
        5. Use a Django Field for Primitive Types.
        6. Use Text by default.
        """
        property_name = Crispr.property_name(prp)
        IMAGEFIELD = dict(
            blank=True,
            field_type="ImageField",
            upload_to=f"images/{app_model_name}/{property_name}",
            null=True,
        )
        FILEFIELD = dict(
            blank=True,
            field_type="FileField",
            upload_to=f"files/{app_model_name}/{property_name}",
            null=True,
        )
        MONEYFIELD = dict(
            decimal_places=2, field_type="DecimalField", max_digits=10
        )

        # Beware 1. The order here is important. Types are selected first come.
        # Beware 2. No field should *python-by-reference* the same Type.
        DJANGO_FIELDS = {
            "Boolean": dict(
                blank=False,
                default=False,
                field_type="BooleanField",
                null=False,
            ),
            "Time": dict(blank=True, field_type="TimeField", null=True),
            "DateTime": dict(blank=True, field_type="DateTimeField", null=True),
            "Date": dict(blank=True, field_type="DateField", null=True),
            "Number": dict(
                blank=True, default=0, field_type="FloatField", null=True
            ),
            "Integer": dict(
                blank=True, default=0, field_type="IntegerField", null=True
            ),
            "Float": dict(
                decimal_places=10, field_type="DecimalField", max_digits=19
            ),
            "Quantity": dict(
                blank=True, default=0, field_type="FloatField", null=True
            ),
            "Duration": dict(blank=True, field_type="DurationField", null=True),
            "URL": dict(
                blank=True, field_type="URLField", max_length=512, null=True
            ),
            "email": dict(field_type="EmailField"),
            "image": IMAGEFIELD,
            "logo": IMAGEFIELD,
            "screenshot": IMAGEFIELD,
            "beforeMedia": FILEFIELD,
            "afterMedia": FILEFIELD,
            "duringMedia": FILEFIELD,
            "minPrice": MONEYFIELD,
            "maxPrice": MONEYFIELD,
            "price": MONEYFIELD,
            "minValue": MONEYFIELD,
            "value": MONEYFIELD,
            "maxValue": MONEYFIELD,
        }
        property_types = self.crispr.property_types_of(prp, self.domain)
        type = None  # Currently unknown.
        # Is there a matching Class Type?
        class_type = DnaOfDjangoModel.dna_of_model_field_type_selector(
            [t for t in property_types if not t.endswith("/Text")],
            [t for t in self.class_backbone if t not in self.crispr.primitives],
        )
        enumerated_type = self.crispr.property_enumerated(prp)
        choices = self.crispr.enumerations_of_by_url(enumerated_type)
        if enumerated_type and class_type and choices:
            # Type Enumerated
            return dict(
                default=choices[0],
                choices=choices,
                field_type="CharField",
                help_text="" if self.no_comments else prp["rdfs:comment"],
                max_length=len(max([c[0] for c in choices], key=len)),
            )
        if class_type:
            # Use the Class Type
            type = class_type
        if not type:
            # Try a Django Model
            type = DnaOfDjangoModel.dna_of_model_field_type_selector(
                [f"{self.domain}/{t}" for t in DJANGO_FIELDS.keys()],
                [t for t in property_types if not "Text" in t],
            )
        if not type:
            # Try a Primitive Type - leave Text til last
            type = DnaOfDjangoModel.dna_of_model_field_type_selector(
                [t for t in property_types if not "Text" in t],
                self.class_backbone,
            )
        if not type:
            # Fall back to Text
            type = f"{self.domain}/Text"
        # Get the name
        type_name = type.replace(f"{self.domain}/", "")
        # Now decide on the best django model Type
        django_type = None
        # Name of the property prefect for a known django model Type.
        if property_name in DJANGO_FIELDS.keys():
            django_type = DJANGO_FIELDS[property_name]
        # Name of the property preordained for long text.
        elif property_name in settings.DNA_LONG_TEXT_FIELDS:
            django_type = dict(blank=True, field_type="TextField")
        # Name of the property preordained char length.
        elif property_name in settings.DNA_SHORT_TEXT_FIELDS.keys():
            django_type = dict(
                blank=True,
                field_type="CharField",
                max_length=settings.DNA_SHORT_TEXT_FIELDS[property_name],
            )
        # Type matches a known django model Type.
        elif type_name in DJANGO_FIELDS.keys():
            django_type = DJANGO_FIELDS[type_name]
        # Standard Text Type.
        elif type_name == "Text":
            django_type = dict(
                blank=True, field_type="CharField", max_length=255
            )
        # ForeignKey to another schema Type.
        else:
            django_type = dict(
                blank=True,
                field_type="ForeignKey",
                null=True,
                related_name=f"{self.app_label.title()}{type_name}_{app_model_name}_{property_name}".lower(),
                related_to=f"{self.app_label.title()}{type_name}",
            )
        django_type["help_text"] = (
            "" if self.no_comments else prp["rdfs:comment"]
        )
        return django_type

    def dna_of_model_fields(self, app_model_name, thing_properties):
        """Return the django fields converted from the properties of a model.

        :param app_model_name: e.g. "AppnameThing"
        :param thing_properties: e.g.
            [{
                '@id': 'http://schema.org/sameAs',
                '@type': 'rdf:Property',
                'http://schema.org/domainIncludes': {'@id': 'http://schema.org/Thing'},
                'http://schema.org/rangeIncludes': {'@id': 'http://schema.org/URL'},
                'rdfs:comment': "Comment...",
                'rdfs:label': 'sameAs'
            }, {
                '@id': 'http://schema.org/url',
                '@type': 'rdf:Property',
                'http://schema.org/domainIncludes': {'@id': 'http://schema.org/Thing'},
                'http://schema.org/rangeIncludes': {'@id': 'http://schema.org/URL'},
                'rdfs:comment': 'URL of the item.',
                'rdfs:label': 'url'
            }, ...]
        """
        fields = dict()
        for prp in thing_properties:
            fields[Crispr.property_name(prp)] = self.dna_of_model_field_type(
                app_model_name, prp
            )
        return fields

    def model_inherits_fields(self, immediately_inherits_from):
        """All fields a model will inherit given its immediate inheritance."""
        inherits_fields = []
        for inheritance in immediately_inherits_from:
            if not inheritance == "models.Model":
                inheritance_dna = self.dna_loaded[inheritance]
                inherits_fields += inheritance_dna["fields_of"].keys()
                inherits_fields += self.model_inherits_fields(
                    inheritance_dna["inherits_from"]
                )
        return inherits_fields

    def model_inherits_from(self, class_of_thing):
        """Return which django model this sub class should inherit from.

        :param class_of_thing: e.g.
            {
              "@id": "http://schema.org/CafeOrCoffeeShop",
              "@type": "rdfs:Class",
              "rdfs:comment": "A cafe or coffee shop.",
              "rdfs:label": "CafeOrCoffeeShop",
              "rdfs:subClassOf": {
                "@id": "http://schema.org/FoodEstablishment"
              }
            }
        """
        # Assume this thing inherits from the base Model (only Thing does!)
        inherits_from = ["models.Model"]
        subclasses_things = Crispr.subclasses_direct(class_of_thing)
        if subclasses_things:
            inherits_from = []
            for subclasses in subclasses_things:
                model_dna = self.dna_of_model(
                    self.crispr.class_of_by_url(subclasses)
                )
                inherits_from.append(model_dna["model_name"])
        return inherits_from

    def dna_of_model_exists(self, app_model_name):
        """Utility to determine if the model_name exists in our structure."""
        return app_model_name in [m for m in self.dna_loaded.keys()]

    def get_dna_of_model_if_exists(self, app_model_name):
        """Utility to get an existing django model if has already been built."""
        model = None
        if self.dna_of_model_exists(app_model_name):
            model = self.dna_loaded[app_model_name]
        return model

    def dna_of_model(self, class_of_thing, options=None):
        """Return a django model given a class object.

        :param class_of_thing: e.g.
            {
                '@id': 'http://schema.org/Thing',
                '@type': 'rdfs:Class',
                'rdfs:comment': 'The most generic type of item.',
                'rdfs:label': 'Thing'
            }
        """
        model_name = class_of_thing.get("rdfs:label")
        app_model_name = f"{self.app_label.title()}{model_name}"
        # Simply return dna of models we have already created (i.e. inherit from).
        model = self.get_dna_of_model_if_exists(app_model_name)
        if model:
            return model
        # Fields
        fields_of = self.dna_of_model_fields(
            app_model_name,
            self.crispr.properties_of_by_url(class_of_thing["@id"]),
        )
        # Establish all the inheritance from other things
        inherits_from = self.model_inherits_from(class_of_thing)
        # Remove fields inherited from parent classes (it's possible because in
        # schema a child class inherits from 2 classes - and any of them
        # are optional - so schema shows properties in the child class that
        # should be present even if you opt not to inherit one of the parents
        # with it).
        all_parent_fields = set(self.model_inherits_fields(inherits_from))
        names_existing = all_parent_fields.intersection(set(fields_of))
        if names_existing:
            for field_name in names_existing:
                fields_of.pop(field_name)
        # If listmode, remove the ForeignKeys. We will handle them as listmode
        # fields instead.
        list_fields = dict()
        if self.elio_list:
            for field_name, field_dna in fields_of.items():
                if field_dna["field_type"] == "ForeignKey":
                    list_fields[field_name] = field_dna.copy()
                    del list_fields[field_name]["blank"]
                    del list_fields[field_name]["null"]
                    del list_fields[field_name]["related_name"]

        if list_fields:
            for field_name in list_fields.keys():
                del fields_of[field_name]
        # Build the dict
        model_dict = {
            "fields_of": fields_of,
            "inherits_from": inherits_from,
            "model_name": app_model_name,
            "list_fields": list_fields,
        }
        # Keep track of the dna of models and fields we have created.
        self.dna_loaded[app_model_name] = model_dict
        return model_dict

    def dna_of_model_by_name(self, thing_name):
        """Conveniently call `dna_of_model` by name instead of class object.

        :param thing_name: e.g. "Thing"
        """
        return self.dna_of_model(self.crispr.class_of_by_name(thing_name))

    def dna_of_models(self, thing_names, type_depth):
        """Build all the DNA of models listed in the settings."""
        picklings_name = self.picklings_name(thing_names, type_depth)
        pick = PickleJar(f"picklings/{self.app_label}", picklings_name)
        # Return the existing DNA.
        if pick.ripe:
            return pick.open()
        # Get the requirements.
        self.class_backbone = self.crispr.dependencies_of_by_names(
            thing_names, type_depth
        )
        # Do each model in any order
        for thing_url in self.class_backbone:
            self.dna_of_model(self.crispr.class_of_by_url(thing_url))
        return pick.pickle(self.dna_loaded)

    def dna_of_models_from_settings(self):
        return self.dna_of_models(list(settings.DNA_THINGS), settings.DNA_DEPTH)
