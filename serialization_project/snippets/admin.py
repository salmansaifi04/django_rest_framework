from django.contrib import admin
from snippets.models import Snippet
# Register your models here.

@admin.register(Snippet)
class SnippetModel(admin.ModelAdmin):
    list_display = ['id', 'title', 'code', 'linenos', 'language', 'style', 'created']
