import django_tables2 as tables
from .models import Document


class DocumentTable(tables.Table):
    class Meta:
        model = Document
