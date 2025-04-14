from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .forms import UploadArquivoForm
import pandas as pd
import io
from django.contrib import messages

def upload_arquivo(request):
    if request.method == 'POST':
        form = UploadArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo_excel = request.FILES['arquivo_excel']
            try:
                df = pd.read_excel(arquivo_excel)
                request.session['dados_excel'] = df.to_json()
                return redirect('exibir_dados')
            except Exception as e:
                messages.error(request, f'Erro ao processar o arquivo: {e}')
        else:
            messages.error(request, 'Por favor, selecione um arquivo válido.')
    else:
        form = UploadArquivoForm()
    return render(request, 'gerenciador_excel/upload_arquivo.html', {'form': form})

def exibir_dados(request):
    if 'dados_excel' in request.session:
        df = pd.read_json(request.session['dados_excel'])
        colunas = df.columns.tolist()
        dados_html = df.to_html(index=False)
        return render(request, 'gerenciador_excel/exibir_dados.html', {'dados_html': dados_html, 'colunas': colunas})
    else:
        return redirect('upload_arquivo')

def remover_coluna(request):
    if request.method == 'POST' and 'coluna_remover' in request.POST and 'dados_excel' in request.session:
        coluna_remover = request.POST['coluna_remover']
        try:
            df = pd.read_json(request.session['dados_excel'])
            if coluna_remover in df.columns:
                df.drop(columns=[coluna_remover], inplace=True)
                request.session['dados_excel'] = df.to_json()
                messages.success(request, f'Coluna "{coluna_remover}" removida com sucesso.')
            else:
                messages.error(request, f'Coluna "{coluna_remover}" não encontrada.')
        except Exception as e:
            messages.error(request, f'Erro ao remover a coluna: {e}')
    return redirect('exibir_dados')

def exportar_excel(request):
    if 'dados_excel' in request.session:
        df = pd.read_json(request.session['dados_excel'])
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="arquivo_modificado.xlsx"'
        return response
    else:
        return redirect('upload_arquivo')