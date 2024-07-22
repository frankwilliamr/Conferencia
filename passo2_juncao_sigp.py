def combinar_arquivos_sem_espacos(arquivo_entrada1, arquivo_entrada2, arquivo_saida):
    # Abrir o arquivo de saída no modo de escrita
    with open(arquivo_saida, 'w', encoding='utf-8') as f_saida:
        # Ler e processar o conteúdo do primeiro arquivo de entrada
        with open(arquivo_entrada1, 'r', encoding='utf-8') as f_entrada1:
            for linha in f_entrada1:
                if linha.strip():  # Escrever a linha se não estiver vazia
                    f_saida.write(linha)
        
        # Ler e processar o conteúdo do segundo arquivo de entrada
        with open(arquivo_entrada2, 'r', encoding='utf-8') as f_entrada2:
            for linha in f_entrada2:
                if linha.strip():  # Escrever a linha se não estiver vazia
                    f_saida.write(linha)
    
    print(f"Arquivos combinados e salvos em {arquivo_saida}")

# Caminhos dos arquivos de entrada
arquivo_entrada1 = "saida/normal_sigp.txt"
arquivo_entrada2 = "saida/exc_sigp.txt"
# Caminho do arquivo de saída
arquivo_saida = "saida/entrada_sigp.txt"

# Combinar os arquivos
combinar_arquivos_sem_espacos(arquivo_entrada1, arquivo_entrada2, arquivo_saida)
