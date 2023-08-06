# -*- encoding: utf-8 -*-
from django.forms import ModelForm
from django.forms.widgets import TextInput, DateInput, DateTimeInput, TimeInput


class AnyEmailInput(TextInput):
    input_type = "email"


class AnyNumberInput(TextInput):
    input_type = "number"


class AnyTelephoneInput(TextInput):
    input_type = "tel"


class AnyDateInput(DateInput):
    input_type = "date"


class AnyDateTimeInput(DateTimeInput):
    input_type = "datetime-local"


class AnyTimeInput(TimeInput):
    input_type = "time"


def every_form(any_model):
    class EveryForm(ModelForm):
        def __init__(self, *args, **kw):
            super().__init__(*args, **kw)
            for f, v in self.fields.items():
                if v.__class__.__name__ == "DateField":
                    self.fields[f].widget = AnyDateInput()
                elif v.__class__.__name__ == "TimeField":
                    self.fields[f].widget = AnyTimeInput()
                elif v.__class__.__name__ == "DateTimeField":
                    self.fields[f].widget = AnyDateTimeInput()
                elif v.__class__.__name__ in [
                    "DurationField",
                    "FloatField",
                    "IntegerField",
                ]:
                    self.fields[f].widget = AnyNumberInput()
                elif v.__class__.__name__ == "EmailField":
                    self.fields[f].widget = AnyEmailInput()
                elif v.__class__.__name__ in [
                    "CharField",
                    "ModelChoiceField",
                    "URLField",
                    "BooleanField",
                    "ImageField",
                ]:
                    pass
                else:
                    print("Needs widget?", v.__class__.__name__)

        field_order = [
            "name",
            "alternateName",
            "disambiguatingDescription",
            "image",
            "description",
            "sameAs",
        ]

        class Meta:
            model = any_model
            exclude = ["pk", "polymorphic_ctype"]

    return EveryForm
