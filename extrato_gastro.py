import sys
from bs4 import BeautifulSoup
import os

def adicionar_separadores_html(caminho_arquivo):
    """
    Adiciona separadores horizontais a um arquivo HTML entre os blocos de títulos.

    :param caminho_arquivo: O caminho para o arquivo HTML a ser modificado.
    :return: Uma string contendo o HTML modificado ou uma mensagem de erro.
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo_html = f.read()
    except FileNotFoundError:
        return f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado."

    soup = BeautifulSoup(conteudo_html, 'html.parser')
    
    tabela_registros = soup.find('table', class_='registros')

    if not tabela_registros:
        return "Erro: A tabela com a classe 'registros' não foi encontrada."

    linhas = tabela_registros.find_all('tr')[2:]
    
    if len(linhas) % 2 != 0:
        print("Aviso: O número de linhas de dados não é par. A formatação pode não ser perfeita.")
    
    for i in range(0, len(linhas), 2):
        if i + 1 < len(linhas):
            nova_linha_separadora = soup.new_tag('tr')
            nova_linha_separadora.append(soup.new_tag('td', colspan='14'))
            nova_linha_separadora.find('td')['style'] = 'padding: 0;'
            nova_linha_separadora.td.append(soup.new_tag('hr'))
            
            linhas[i+1].insert_after(nova_linha_separadora)

    return str(soup)

if __name__ == "__main__":
    # Pergunta ao usuário o caminho do arquivo
    arquivo_original = input("Por favor, digite o caminho completo do arquivo HTML que deseja modificar: ")
    
    # Cria o nome do arquivo de saída
    dir_name, file_name = os.path.split(arquivo_original)
    saida_modificada = os.path.join(dir_name, "modificado_" + file_name)
    
    html_modificado = adicionar_separadores_html(arquivo_original)

    if html_modificado.startswith("Erro:"):
        print(html_modificado)
    else:
        try:
            with open(saida_modificada, 'w', encoding='utf-8') as f:
                f.write(html_modificado)
            print(f"Arquivo modificado salvo com sucesso como '{saida_modificada}'.")
        except IOError as e:
            print(f"Erro ao salvar o arquivo: {e}")