# /* cSpell:disable 

import os
import time
from tqdm import tqdm
import urllib.parse



def buscar_e_escrever_linhas_com_palavra_chave(nome_arquivo, palavra_chave):
    linhas_relevantes = []
    erros_decodificacao = 0
    with open(nome_arquivo, 'rb') as arquivo:
        for linhas_bytes in arquivo:
            try:
                linha = linhas_bytes.decode('utf-8')
                if palavra_chave in linha:
                    linhas_relevantes.append(linha.strip())
            except UnicodeDecodeError:
                erros_decodificacao += 1
            return linhas_relevantes, erros_decodificacao            
        
def limpar_nome_arquivo(nome_arquivo):
    caracteres_invalidos = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in caracteres_invalidos:
        nome_arquivo = nome_arquivo.replace(char, '_')
    return nome_arquivo

def main(): 
    pasta_db = "db" 

    palavra_chave = input("Digite o texto que deseja usar como palavra chave: ")
    palavra_chave_encoded = urllib.parse.quote(palavra_chave)

    nome_arquivo_saida = f"{limpar_nome_arquivo(palavra_chave_encoded)}.txt"        

    arquivos_txt = [arquivo for arquivo in os.listdir(pasta_db) if arquivo.endswith('.txt')] 

    with tqdm(total=len(arquivos_txt), desc="Progesso de pesquisa") as progesso_barra:
        total_linhas_encontradas = 0 
        total_erros_decodificacao = 0
        with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
            for arquivo_txt in arquivos_txt:
                caminho_arquivo = os.path.join(pasta_db, arquivo_txt)
                linhas_relevantes, erros_decodificacao = buscar_e_escrever_linhas_com_palavra_chave(caminho_arquivo, palavra_chave)
                total_linhas_encontradas += len(linhas_relevantes)
                total_erros_decodificacao += erros_decodificacao
                
                if linhas_relevantes:

                    arquivo_saida.write(f"-\n")
                    arquivo_saida.writelines("\n".join(linhas_relevantes)) 
                    arquivo_saida.write("\n\n")
                    progesso_barra.update(1)
                    time.sleep(0.1)

    if total_erros_decodificacao == 0:
        print("Nenhuma linha encontrada.")
    else:
        print(f"Processo concluido. {total_linhas_encontradas} linhas relevantes foram encontradas e escritas no arquivo '{nome_arquivo_saida}'.")

    if total_erros_decodificacao > 0:
        print(f"Total de errod de deocodificação: {total_erros_decodificacao}")


if __name__ == "__main__":
    main()

