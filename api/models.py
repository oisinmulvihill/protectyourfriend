"""
For price storage I will use integers represent pence. This is easier to work
with and gets around rounding problems. Price formating can be handled when
displayed to the end user.

"""
from datetime import datetime

from django.db import utils
from django.db import models


class DuplicateError(Exception):
    """Raised when attempt to add a non unique entry."""


class PolicyType(models.Model):
    """The type of pet insurance policy we offer and the base monthly cost for
    each.

    I try to keep the lower level db query operation hide at this layer.

    """
    name = models.CharField(max_length=64, unique=True)

    base_price = models.IntegerField()

    created = models.DateTimeField(default=datetime.utcnow)

    @classmethod
    def add(cls, name, base_price):
        """Add a new entry.

        If the policy name is present already then

        """
        # Basic validation of inputs:
        _name = name.lower().strip() if name else name
        if not _name:
            raise ValueError("Policy name is required!")

        _base = int(base_price)
        if _base < 1:
            raise ValueError("The base price must be above 1!")

        policy = cls(name=_name, base_price=_base)
        try:
            policy.save()

        except utils.IntegrityError as error:
            raise DuplicateError(f"{error}")

        return policy

    @classmethod
    def get(cls, name):
        """Recover an existing entry.
        """
        return cls.objects.filter(name=name).first()

    @classmethod
    def policies(cls):
        """Return all the supported policy types we price for."""
        return cls.objects.order_by('-created') or []

    def __str__(self):
        return f"{self.name}"


class Breed(models.Model):
    """Used to store the price modifying data on the cat and dog breeds we
    will insure.

    """
    species = models.CharField(max_length=10)

    name = models.CharField(max_length=128)

    risk_gradient = models.IntegerField()

    created = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        unique_together = (('species', 'name'),)

    @classmethod
    def add(cls, species, name, risk_gradient):
        """Add a new breed entry.

        The species and name must be unique.

        """
        # Basic validation of inputs:
        _species = species.lower().strip() if species else species
        if not _species:
            raise ValueError("Breed species is required!")

        _name = name.lower().strip() if name else name
        if not _name:
            raise ValueError("Breed name is required!")

        _gradient = int(risk_gradient)
        if _gradient < 1:
            raise ValueError("The risk gradient must 1 or more!")

        breed = cls(
            species=_species,
            name=_name,
            risk_gradient=_gradient
        )
        breed.save()

        return breed

    @classmethod
    def get(cls, species, name):
        """Recover an existing breed entry.
        """
        return cls.objects.filter(
            species=species, name=name
        ).first()

    @classmethod
    def breeds(cls):
        """Return all the supported breeds we price for.
        """
        return cls.objects.order_by('-created') or []

    def __str__(self):
        return f"{self.species}: {self.name}"
