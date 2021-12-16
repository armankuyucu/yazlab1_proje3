from django import forms
from .models import Document


class UploadFileForm(forms.Form):
    class Meta:
        model = Document
        fields = ('title','pdf')

    # title = forms.CharField(max_length=50)
    # file = forms.FileField()