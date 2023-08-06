# -*- encoding: utf-8 -*
from django.conf import settings
from dna.dna import DnaOfDjangoModel
from dna.replicate import every_model


dna = DnaOfDjangoModel("dna/tests/mocks/space.jsonld", "dna").dna_of_models(
    [
        "Thing",
        "Universe",
        "Galaxy",
        "SolarSystem",
        "Sun",
        "Planet",
        "Moon",
        "Belt",
        "Asteroid",
        "Enumeration",
        "Interestingness",
        "Satellite",
        "GPS",
    ],
    0,
)
every_model(dna, "dna")
