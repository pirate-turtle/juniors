from django.contrib import admin
from .models import ReferenceLink

@admin.register(ReferenceLink)
class ReferenceLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')