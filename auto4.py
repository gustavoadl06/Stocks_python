# Importando bibliotecas necessárias
import requests
from bs4 import BeautifulSoup
import pandas as pd


# Lista das ações desejadas
list_stocks = {'bbas3','bbdc4','csmg3', 'itub3','sapr4','sula11','taee11','alup4','petr3','brsr6','sanb3','trpl4','sanb3'}


# Lista para armazenar os dados das ações que irão no Data Frame
dictionary_data = []

# Função para obter indicadores de uma ação
def get_indicators(stock):

    # Definindo o User-Agent para evitar bloqueios
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'
    }
     # URL da página da ação no StatusInvest
    url = f'https://statusinvest.com.br/acoes/{stock}'

     # Fazendo uma requisição HTTP com headers personalizados
    site = requests.get(url, headers=headers)

    # Criando um objeto BeautifulSoup para analisar o HTML da página
    soup = BeautifulSoup(site.content, 'html.parser')

    # Extraindo os indicadores da página usando seletores específicos
    actual_value = soup.find('strong', class_='value').get_text().strip() 
    dividend_yield_div = soup.find('div', {'title': 'Dividend Yield com base nos últimos 12 meses'})
    dividend_yield = dividend_yield_div.find('strong', class_='value').get_text().strip()

    vpa_div = soup.find('div', {'title': 'Indica qual o valor patrimonial de uma ação.'})    
    vpa = vpa_div.find('strong', class_='value d-block lh-4 fs-4 fw-700').get_text().strip() # (VPA)

    lpa_div = soup.find('div', {'title': 'Indicar se a empresa é ou não lucrativa. Se este número estiver negativo, a empresa está com margens baixas, acumulando prejuízos.'})
    lpa = lpa_div.find('strong', class_='value d-block lh-4 fs-4 fw-700').get_text().strip()#earnings per share (LPA)


     # Armazenando os dados em um dicionário
    data = { "Stock" : stock,
             "Value" : actual_value,  
             "DY" : dividend_yield,
              "VPA": vpa,
              "LPA": lpa          }

    dictionary_data.append(data)

    print(f'------Indicadores da ação:{stock}-----')
    print('Stock value:', actual_value)
    print('Dividend Yield:', dividend_yield)
    print('Price per Book Value:', vpa)
    print('Earnings per Share:', lpa) 
    print('\n')

#Loop que percorre a função passando de ação para ação da lista de ações.
for stock in list_stocks:
    get_indicators(stock)
    

# Convertendo os dados coletados e adicionados ao dicionário em um DataFrame (pandas).
df = pd.DataFrame(dictionary_data)

print(df)

# Salvando o DataFrame em um arquivo Excelm, o mesmo gera o arquivo.
df.to_excel("Indicadores.xlsx")
