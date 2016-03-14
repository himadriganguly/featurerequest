from django.db import models

# Create your models here.


class Client(models.Model):
    name = models.CharField(
        max_length=150,
        help_text="Enter the name of the client",
        unique=True,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=150,
        help_text="Enter the name of the Product",
        unique=True,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name


class FeatureRequest(models.Model):
    title = models.CharField(
        max_length=300,
        help_text="Enter a short, descriptive name of the feature request.",
        blank=False,
        null=False,
    )

    desc = models.TextField(
        blank=False,
        null=False,
    )

    priority = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    targetdate = models.DateField(
        blank=False,
        null=False,
    )

    url = models.URLField(
        blank=True,
        null=True,
    )

    client = models.ForeignKey(
        Client,
        blank=False,
        null=False,
        related_name='tickets'
    )

    productarea = models.ForeignKey(
        Product,
        blank=False,
        null=False,
        related_name='tickets',
    )

    class Meta:
        ordering = ['priority']
        unique_together = (("title", "client"),)  # ("priority", "client")

    def __str__(self):
        return self.title
