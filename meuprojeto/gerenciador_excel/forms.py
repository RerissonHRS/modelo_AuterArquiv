from django import forms

class UploadArquivoForm(forms.Form):
    arquivo_excel = forms.FileField(label='Selecione o arquivo Excel')