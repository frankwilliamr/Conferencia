import re

# Lista de exceções de proventos
exc_proventos = [
   
    "VALE TRANS",
    "EST EC SALBASE DA1",
    "EST EC SALBASE DA2",
    
    # Adicione mais tipos de proventos conforme necessário
]

# Função para extrair informações dos vencimentos
def extrair_informacoes(texto, exc_proventos):
    # Padrão de expressão regular para buscar e capturar as informações
    padrao_dados = r"Matrícula:\s*(\d+).*?(?=(?:\n\s*\n|\Z))"
    padrao_vencimentos = r"(\d+)\s+(" + '|'.join(map(re.escape, exc_proventos)) + r")\s+([\d.,]+)"

    # Encontrar todas as correspondências no conteúdo
    matches_dados = re.findall(padrao_dados, texto, re.DOTALL)
    matches_vencimentos = re.findall(padrao_vencimentos, texto)

    # Processar os valores encontrados
    resultados = []

    # Adicionar vencimentos à lista de resultados
    for match_vencimento in matches_vencimentos:
        referencia = match_vencimento[0]
        tipo = match_vencimento[1]
        valor_bruto = match_vencimento[2]

        # Formatar o valor removendo os pontos e substituindo a vírgula por ponto
        valor_formatado = valor_bruto.replace(".", "").replace(",", ".")

        # Adicionar à lista de resultados com indicação de tipo (Vencimento)
        if matches_dados:
            matricula = matches_dados[0]
            resultados.append((referencia, valor_formatado, matricula, tipo))

    return resultados

# Função para processar um arquivo com múltiplos exemplos
def processar_arquivo(arquivo_entrada, arquivo_saida, exc_proventos):
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Dividir o conteúdo em exemplos individuais (separados por linhas em branco)
    exemplos = conteudo.strip().split('\n\n')

    # Para cada exemplo, extrair as informações de vencimentos
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for exemplo in exemplos:
            infos = extrair_informacoes(exemplo, exc_proventos)
            if not infos:
                print(f"Nenhuma informação extraída para o exemplo:\n{exemplo}")
            for info in infos:
                f.write(f"Matrícula: {info[2]}, Referência: {info[0]}, Valor Formatado: {info[1]}\n")
            

    print(f"Informações extraídas e salvas em {arquivo_saida}")

# Caminho do arquivo de entrada com múltiplos exemplos
arquivo_entrada = "sigp.txt"
# Caminho do arquivo de saída
arquivo_saida = "saida/exc_sigp.txt"

# Verificar se os caminhos dos arquivos estão corretos
print(f"Arquivo de entrada: {arquivo_entrada}")
print(f"Arquivo de saída: {arquivo_saida}")

# Processar o arquivo de entrada e salvar as informações de vencimentos no arquivo de saída
processar_arquivo(arquivo_entrada, arquivo_saida, exc_proventos)
