from django.contrib import admin
from .models import Client, Product, FeatureRequest


class FeatureRequestAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "productarea",
        "targetdate",
        "priority",
    )

# Register your models here.
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(FeatureRequest, FeatureRequestAdmin)
