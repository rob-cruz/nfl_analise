#cel 1
 #Primeiro, importamos as bibliotecas e definimos a URL principal:
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
adapter = HTTPAdapter(max_retries=retries)

session.mount('https://', adapter)
session.mount('http://', adapter)


url_base = 'https://www.nfl.com/teams/buffalo-bills/roster'
#https://www.reclameaqui.com.br/empresa/magazine-luiza-loja-online/lista-reclamacoes/

#cel 2
start_time = time.time()
#Em seguida, definimos uma função para extrair as informações de uma reclamação a partir de sua URL:


#def extrair_dados_reclamacao(url):

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
req = requests.get(url_base, headers=headers, verify=False)
soup = BeautifulSoup(req.content, 'html.parser')
soup

tabela = soup.find('tbody').text.strip()
table = soup.find('tbody')
numero = soup.td
atribute = numero.attrs
print(atribute)
'''
status = soup.find('span', {'data-testid': 'complaint-location'}).text.strip()
altura = soup.find('span', {'data-testid': 'complaint-creation-date'}).text.strip().split('\n')[0]
peso = soup.find('span', {'class': 'sc-lzlu7c-12 iwABCI'}).text.strip()
experiencia = [tag.text.strip() for tag in soup.find_all('div', {'class': 'sc-lzlu7c-11 gjquMH'})]
faculdade = soup.find('p', {'class': 'sc-lzlu7c-17 fRVYjv'}).text.strip()
dados_reclamacao = {
    'Nome': nome,
    '#NUMero': numero,
    'Localização': status,
    'Data/Hora': altura,
    'ID da Reclamação': peso,
    'Categorias': experiencia,
    'Mensagem': faculdade
}
'''
nome = []
nume = []
stat = []
altu = []
peso = []
expe = []
facu = []

for row in table.findAll("tr"): #para tudo que estiver em <tr>
    cells = row.findAll('td') #variável para encontrar <td>
    if len(cells)==7: #número de colunas
        nome.append(cells[0].find('a',{'class':'nfl-o-roster__player-name nfl-o-cta--link'}).text.strip) #iterando sobre cada linha
        nume.append(cells[1].find(text=True))
        stat.append(cells[2].find(text=True))
        altu.append(cells[3].find(text=True))
        peso.append(cells[4].find(text=True))
        expe.append(cells[5].find(text=True))
        facu.append(cells[6].find(text=True))

import pandas as pd

df = pd.DataFrame(index=nome, columns=['nome'])
df['nome']=nome
df['nume']=nume
df['stat']=stat
df['altu']=altu
df['peso']=peso
df['expe']=expe
df['facu']=facu
df.head()


#return dados_reclamacao
print(table)
print(soup)

table.find("tr").text.strip()
#print(dados_reclamacao)


#cel3

#Nessa função, fazemos uma requisição GET à página da reclamação, utilizando a biblioteca requests, e depois usamos a BeautifulSoup para extrair as informações. A função retorna um dicionário com as informações extraídas.

#Agora, precisamos de outra função para extrair as URLs das reclamações da página atual:


def extrair_urls_reclamacoes(pagina):

    #print(pagina)
    #req = requests.get(pagina)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    req = requests.get(pagina, verify=False, headers=headers)
    soup = BeautifulSoup(req.content, 'html.parser')


    urls_reclamacoes = []

    reclamacoes = soup.find_all('div', {'class': 'sc-1pe7b5t-0 eJgBOc'})

    for reclamacao in reclamacoes:
        url = reclamacao.find('a').get('href')
        url_completa = f'https://www.reclameaqui.com.br{url}'
        urls_reclamacoes.append(url_completa)

    return urls_reclamacoes
    #print(url_completa)
    #print(url)




#Essa função também faz uma requisição GET à página, utiliza a BeautifulSoup para extrair as URLs das reclamações e retorna uma lista com essas URLs completas.

#cel4

#Agora, podemos utilizar essas duas funções para iterar pelas páginas do Reclame Aqui e extrair as informações:


'''____________________________________________________________________________________________________________'''
dados_totais = []
pagina_atual = 1

while True:
    pagina = f'{url_base}?pagina={pagina_atual}'
    urls_reclamacoes = extrair_urls_reclamacoes(pagina)

    #if not urls_reclamacoes:
    if not urls_reclamacoes:
        break

    for url in urls_reclamacoes:
        dados_reclamacao = extrair_dados_reclamacao(url)
        dados_totais.append(dados_reclamacao)
    #print(urls_reclamacoes)
    print(f'Página {pagina_atual} concluída.')


    pagina_atual += 1
    #print(dados_reclamacao)

#cel5

#Por fim, convertemos os dados obtidos em uma estrutura do tipo DataFrame, utilizando a biblioteca pandas, e exportamos para um arquivo CSV:
df = pd.DataFrame(dados_totais)
df.to_csv('reclamacoes_vivo.csv', index=False, encoding = "ISO-8859-1")

#Além disso, para medir o tempo de execução, podemos adicionar um timer no início e no final do script, e imprimir a diferença:
end_time = time.time()
print(f'Tempo de execução: {end_time - start_time:.2f} segundos')

df.head()


