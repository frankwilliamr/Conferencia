from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO

# Função para processar um arquivo no formato dado
def processar_arquivo(nome_arquivo):
    dados = {}
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha_num, linha in enumerate(arquivo, start=1):
            partes = linha.strip().split(', ')
            if len(partes) == 3:
                matricula_str = partes[0].split(': ')[1]
                referencia_str = partes[1].split(': ')[1]
                valor_formatado_str = partes[2].split(': ')[1]
                
                try:
                    matricula = int(matricula_str)
                    referencia = int(referencia_str)
                    valor_formatado = float(valor_formatado_str)
                    
                    if matricula not in dados:
                        dados[matricula] = {}
                    
                    dados[matricula][referencia] = valor_formatado
                
                except ValueError:
                    print(f"Erro de conversão na linha {linha_num}: {linha}")
            
            else:
                print(f"Formato inválido na linha {linha_num}: {linha}")
    
    return dados

# Função para comparar dois conjuntos de dados e gerar o resultado
def comparar_arquivos(arquivo1, arquivo2):
    dados1 = processar_arquivo(arquivo1)
    dados2 = processar_arquivo(arquivo2)
    
    resultados = {}
    
    # Iterar sobre as matrículas presentes nos dados do arquivo 1
    for matricula in dados1:
        if matricula in dados2:
            # Comparar referências para esta matrícula
            resultados[matricula] = []
            for referencia in set(dados1[matricula].keys()).union(set(dados2[matricula].keys())):
                #if referencia != 0:  # Ignorar a referência 20
                    valor1 = dados1[matricula].get(referencia, 0.0)
                    valor2 = dados2[matricula].get(referencia, 0.0)
                    
                    diferenca = valor1 - valor2
                    if diferenca != 0.0:
                        resultados[matricula].append((referencia, valor1, valor2, diferenca))
        
        else:
            # Se a matrícula do arquivo 1 não existe no arquivo 2, comparar todas as referências do arquivo 1
            resultados[matricula] = []
            for referencia, valor1 in dados1[matricula].items():
                #if referencia != 0:  # Ignorar a referência 20
                    resultados[matricula].append((referencia, valor1, 0.0, valor1))
    
    # Verificar se há matrículas no arquivo 2 que não estão no arquivo 1
    for matricula in dados2:
        if matricula not in dados1:
            resultados[matricula] = []
            for referencia, valor2 in dados2[matricula].items():
                #if referencia != 20:  # Ignorar a referência 20
                    resultados[matricula].append((referencia, 0.0, valor2, -valor2))
    
    return resultados

# Função para gerar o PDF com os resultados
def gerar_pdf(resultados, nome_arquivo):
    c = canvas.Canvas(nome_arquivo, pagesize=letter)
    
    # Configurações da tabela
    c.setFont("Helvetica-Bold", 12)
    
    for matricula, diffs in resultados.items():
        if diffs:  # Verifica se há diferenças para esta matrícula
            c.drawString(72, c._pagesize[1] - 50, f"Matrícula: {matricula}")
            c.setFont("Helvetica", 10)
            
            data = [['Referência', 'SIGP', 'Vitruvio', 'Diferença']]
            for diff in diffs:
                #if diff[0] != 20:  # Ignorar a referência 20
                    if diff[3] != 0.0:  # Verifica se a diferença não é 0.0
                        data.append([str(diff[0]), str(diff[1]), str(diff[2]), str(diff[3])])
            
            # Estilo da tabela
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            
            # Criando a tabela
            table = Table(data)
            table.setStyle(style)
            
            # Coordenadas para posicionar a tabela no PDF
            table.wrapOn(c, 800, 600)
            table.drawOn(c, 72, c._pagesize[1] - 100 - (len(data) * 20))  # Posição da tabela no PDF
            
            # Mostra a página atual e inicia uma nova
            c.showPage()
    
    # Salvar o PDF
    c.save()

# Exemplo de uso:
if __name__ == '__main__':
    resultado = comparar_arquivos('saida/filtered_entrada_sigp.txt', 'saida/filtered_entrada_vitruvio.txt')
    gerar_pdf(resultado, 'resultados/resultado_comparacao.pdf')

    print("PDF gerado com sucesso.")
