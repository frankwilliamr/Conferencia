import re

# Função para ler os tipos de proventos do arquivo
def ler_tipos_proventos(caminho_tipos_proventos):
    with open(caminho_tipos_proventos, 'r', encoding='utf-8') as file:
        tipos_proventos = [line.strip() for line in file.readlines()]
    return tipos_proventos

# Função para extrair informações dos vencimentos
def extrair_informacoes(texto, tipos_proventos):
    # Padrão de expressão regular para buscar e capturar as informações
    padrao_dados = r"Matrícula:\s*(\d+).*?(?=(?:\n\s*\n|\Z))"
    padrao_vencimentos = r"(\d+)\s+(" + '|'.join(map(re.escape, tipos_proventos)) + r")\s+(\d+(?:/\d+)?|\d+,\d+)\s+([\d.,]+)"

    # Encontrar todas as correspondências no conteúdo
    matches_dados = re.findall(padrao_dados, texto, re.DOTALL)
    matches_vencimentos = re.findall(padrao_vencimentos, texto)
    
    # Processar os valores encontrados
    resultados = []
    
    # Adicionar vencimentos à lista de resultados
    for match_vencimento in matches_vencimentos:
        referencia = match_vencimento[0]
        tipo = match_vencimento[1]
        ref_numero = match_vencimento[2]
        valor_bruto = match_vencimento[3]
        
        # Formatar o valor removendo os pontos e substituindo a vírgula por ponto
        valor_formatado = valor_bruto.replace(".", "").replace(",", ".")
        
        # Adicionar à lista de resultados com indicação de tipo (Vencimento)
        if matches_dados:
            matricula = matches_dados[0]
            resultados.append((referencia, ref_numero, valor_formatado, matricula, "Vencimento"))
    
    return resultados

# Função para processar um arquivo com múltiplos exemplos
def processar_arquivo(arquivo_entrada, arquivo_saida, caminho_tipos_proventos):
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Ler os tipos de proventos do arquivo
    tipos_proventos = ler_tipos_proventos(caminho_tipos_proventos)
    
    # Dividir o conteúdo em exemplos individuais (separados por linhas em branco)
    exemplos = conteudo.strip().split('\n\n')
    
    # Para cada exemplo, extrair as informações de vencimentos
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for exemplo in exemplos:
            infos = extrair_informacoes(exemplo, tipos_proventos)
            for info in infos:
                f.write(f"Matricula: {info[3]}, Referencia: {info[0]},  Valor Formatado: {info[2]}\n")
            
            
    print(f"Informações extraídas e salvas em {arquivo_saida}")

# Caminho do arquivo de entrada com múltiplos exemplos
arquivo_entrada = "sigp.txt"
# Caminho do arquivo de saída
arquivo_saida = "saida/normal_sigp.txt"
# Caminho do arquivo contendo os tipos de proventos
caminho_tipos_proventos = 'tipos_proventos.txt'

# Processar o arquivo de entrada e salvar as informações de vencimentos no arquivo de saída
processar_arquivo(arquivo_entrada, arquivo_saida, caminho_tipos_proventos)
