from django import forms
from .models import UploadDataModel
from django.core.files.base import ContentFile


class UploadDataForm(forms.ModelForm):
    class Meta:
        model = UploadDataModel
        fields = ['document']
        # widgets = {
        #     'document':forms.FileField()
        #     }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.created_by = user
        
        if commit:
            instance.save()
        
        if self.cleaned_data.get('document'):
            print("herrrrrr")
            chunk_size = 64 * 1024  # 64 KB
            with instance.document.open('rb') as file:
                while True:
                    data_chunk = file.read(chunk_size)
                    if not data_chunk:
                        break
                    
                    instance.document.save(instance.document.name, ContentFile(data_chunk), save=False)
        
        
        if commit:
            instance.save()
        return instance
