"""Core views."""
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import FileUpload

from .forms import FileUploadForm
from .dataProcessing_utils import Get_attribute
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

                data_list = []
                text_file = extract_text_from_pdf(file_path)
                get_obj = Get_attribute(text_file)
                datas1 = get_obj.process1()

                if datas1.get('data_process'):
                    print('Hallo bhai, ', datas1.get('data_process'))
                    data_list.append(datas1.get('data'))
                    return render(request, self.template_name, {"data_list": data_list, "form": form})

                datas2 = get_obj.process2()
                if datas2.get('data_process'):
                    data_list.append(datas2.get('data'))
                    return render(request, self.template_name, {"data_list": data_list, "form": form})

                datas3 = get_obj.process3()
                if datas3.get('data_process'):
                    data_list.append(datas3.get('data'))
                    return render(request, self.template_name, {"data_list": data_list, "form": form})
                else:
                    return render(request, self.template_name, {"form": form, "error": "PDF ERROR"})
            except Exception as e:
                print('<><><><><><><><>')
                print('Error', e)
