from django.core.validators import FileExtensionValidator
from django.forms import ModelForm
from .models import FileUpload
from django.forms import forms


# class Upload_pdfFile(forms.Form):
#     file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])])


class FileUploadForm(ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']
