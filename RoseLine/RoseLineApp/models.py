from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Breed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Horse(models.Model):

    class Gender(models.TextChoices):
        MALE = "M", "Stallion"
        FEMALE = "F", "Mare"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Still Owned"
        SOLD = "SOLD", "Sold"
        VOIDED = "VOIDED", "Voided"

    class Personality(models.TextChoices):
        ALOOF = "ALOOF", "Aloof"
        BRONCO = "BRONCO", "Bronco"
        CAREFREE = "CAR", "Carefree"
        CLINGY = "CLINGY", "Clingy"
        DANGEROUS = "DAN", "Dangerous"
        DISTRUSTFUL = "DIS", "Distrustful"
        EXTROVERT = "EXT", "Extrovert"
        FEARFUL = "FEA", "Fearful"
        FRESH = "FRESH", "Fresh"
        HOTBLOODED = "HOT", "Hotblooded"
        JUMPY = "JUMPY", "Jumpy"
        KICKHAPPY = "KICK", "Kickhappy"
        LAZY = "LAZY", "Lazy"
        MINIMALIST = "MINI", "Minimalist"
        MUDMAGNET = "MUD", "Mudmagnet"
        SENSITIVE = "SEN", "Sensitive"
        SERENE = "SER", "Serene"
        SPIRITED = "SPI", "Spirited"
        RANCHHAND = "RAN", "Ranchhand"
        SHOWHORSE = "SHOW", "Showhorse"
        TRACKER = "TRA", "Tracker"
        GUARDIAN = "GUA", "Guardian"
        FERAL = "FERAL", "Feral"
        INYOURPOCKET = "POCKET", "Inyourpocket"
        TRAILBOSS = "TRAIL", "Trailboss"

    # --- identity ---
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    brand_tag = models.CharField(max_length=50, blank=True, null=True)
    coat_name = models.CharField(max_length=100)
    genetics = models.CharField(max_length=255)

    # --- core traits ---
    gender = models.CharField(max_length=1, choices=Gender.choices)

    breed = models.ForeignKey(
        Breed,
        on_delete=models.PROTECT,
        related_name="horses"
    )

    personality = models.CharField(
        max_length=15,
        choices=Personality.choices,
        default=Personality.MINIMALIST
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

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Horse.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    stable_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username