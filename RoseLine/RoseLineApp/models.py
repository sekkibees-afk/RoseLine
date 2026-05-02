from django.db import models
from django.contrib.auth.models import User


class Breed(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Horse(models.Model):

    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Still Owned"
        SOLD = "SOLD", "Sold"
        VOIDED = "VOIDED", "Voided"

    class Personality(models.TextChoices):
        CALM = "CALM", "Calm"
        AGGRESSIVE = "AGG", "Aggressive"
        NERVOUS = "NER", "Nervous"
        FRIENDLY = "FRI", "Friendly"
        STUBBORN = "STU", "Stubborn"

    # --- identity ---
    name = models.CharField(max_length=100)

    brand_tag = models.CharField(max_length=50, blank=True, null=True)

    coat_name = models.CharField(max_length=100)

    genetics = models.CharField(max_length=255)

    # --- core traits ---
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices
    )

    breed = models.ForeignKey(
        Breed,
        on_delete=models.PROTECT,
        related_name="horses"
    )

    personality = models.CharField(
        max_length=15,
        choices=Personality.choices,
        default=Personality.CALM
    )

    # --- lineage ---
    sire = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sire_offspring"
    )

    dam = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="dam_offspring"
    )

    is_purebred = models.BooleanField(default=True)

    # --- ownership ---
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="horses"
    )

    # --- lifecycle ---
    conceived_date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    # --- progression ---
    max_stat = models.BooleanField(default=False)
    trained = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name