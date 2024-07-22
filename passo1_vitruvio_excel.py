import pandas as pd
import math

# Função para ler o arquivo Excel e salvar em TXT com formato específico
def excel_para_txt_formatado(caminho_excel, caminho_txt, colunas):
    # Ler o arquivo Excel
    df = pd.read_excel(caminho_excel)

    # Selecionar as colunas específicas
    df_selecionado = df[colunas]

    # Agrupar por 'Matrícula' e 'Código Verba', somando os valores
    df_agrupado = df_selecionado.groupby(['Matrícula', 'Código Verba']).sum().reset_index()

    # Abrir (ou criar) o arquivo TXT para escrita
    with open(caminho_txt, 'w') as f:
        for index, row in df_agrupado.iterrows():
            # Limpar a matrícula: remover 0 no início e - no final
            matricula = str(row['Matrícula']).lstrip('0').replace('.', '').replace('-', '')
            referencia = row['Código Verba']
            if isinstance(referencia, (int, float)) and not math.isnan(referencia):
                referencia = int(referencia)  # Convertendo para inteiro se possível
            else:
                referencia = 0
            valor_formatado = abs(row['Valor'])
            linha_formatada = f"Matricula: {matricula}, Referencia: {referencia}, Valor Formatado: {valor_formatado}\n"
            f.write(linha_formatada)

# Exemplo de uso
caminho_excel = 'vitruvio.xlsx'
caminho_txt = 'saida/entrada_vitruvio.txt'
colunas = ['Matrícula', 'Código Verba', 'Valor']  # Ajuste os nomes das colunas conforme necessário

excel_para_txt_formatado(caminho_excel, caminho_txt, colunas)
