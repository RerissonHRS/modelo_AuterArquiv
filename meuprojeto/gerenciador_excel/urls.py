from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_arquivo, name='upload_arquivo'),
    path('exibir/', views.exibir_dados, name='exibir_dados'),
    path('remover_coluna/', views.remover_coluna, name='remover_coluna'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),
]