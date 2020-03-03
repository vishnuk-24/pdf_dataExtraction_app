"""Core views."""
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import FileUpload

from .forms import FileUploadForm
from .dataProcessing_utils import get_attributes_from_textfile_process1, \
    get_attributes_from_textfile_process2, get_attributes_from_textfile_process3
from .extraction_utils import extract_text_from_pdf


class IndexView(View):
    """Indexview for testing django view"""

    template_name = "core/index.html"
    form_class = FileUploadForm

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = form.cleaned_data['file']
                file_name, file_type = file.name.rsplit(".", 1)
                file_object = FileUpload(file=file, filename=file_name)
                file_object.save()
                file_path = os.path.join(settings.BASE_DIR, file_object.file.path)
                print('file_path', file_path)
                self.text_file = extract_text_from_pdf(file_path)
                datas = get_attributes_from_textfile_process1(self.text_file)
                if not datas:
                    datas = get_attributes_from_textfile_process2(self.text_file)
            except Exception as e:
                print('Error', e)
                # return render(request, self.template_name, {"form": form, "error": "PDF ERROR"})
                try:
                    datas = get_attributes_from_textfile_process2(self.text_file)
                except Exception as e:
                    print('Error', e)
                    datas = get_attributes_from_textfile_process3(self.text_file)
            if datas:
                data_list = []
                data_list.append(datas)
                return render(request, self.template_name, {"data_list": data_list, "form": form})

# path = os.path.abspath(request.FILES['pdf'].file.name)
