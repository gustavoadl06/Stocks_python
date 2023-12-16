# Importing necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

# List of desired stocks
list_stocks = {'bbas3', 'bbdc4', 'csmg3', 'itub3', 'sapr4', 'sula11', 'taee11', 'alup4', 'petr3', 'brsr6'}

# Creating an empty list to store data dictionaries
dictionary_data = []

# Function to format money values
def format_money(value):
    return f'R$ {value}'

# Function to format percentage values
def format_percentage(dividend_yield):
    return f'{dividend_yield}%'

# Function to calculate intrinsic value
def intrinsic_value_calculous(lpa, vpa):
    result = (float(lpa.replace(',', '')) * float(vpa.replace(',', '')) * 22.5)
    raiz = math.sqrt(result)
    raiz /= 100
    result = round(raiz, 2)
    return result

# Function to calculate opportunity value
def oportunity_value_calculous(intrinsic_value, actual_value):
    oportunity_calculous = (intrinsic_value - (float(actual_value.replace(',', '.')))) / (float(actual_value.replace(',', '.')))
    oportunity_calculous_percentage = round(oportunity_calculous * 100, 2)
    return oportunity_calculous_percentage

# Function to scrape data from the website
def get_indicators(stock):
    # Defining user agent in headers to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'
    }
    # Constructing the URL for the stock
    url = f'https://statusinvest.com.br/acoes/{stock}'
    # Making a request to the website
    site = requests.get(url, headers=headers)
    # Parsing the HTML content using BeautifulSoup
    soup = BeautifulSoup(site.content, 'html.parser')

    # Extracting relevant data from the HTML
    actual_value = soup.find('strong', class_='value').get_text().strip()
    dividend_yield_div = soup.find('div', {'title': 'Dividend Yield com base nos últimos 12 meses'})
    dividend_yield = dividend_yield_div.find('strong', class_='value').get_text().strip()
    vpa_div = soup.find('div', {'title': 'Indica qual o valor patrimonial de uma ação.'})
    vpa = vpa_div.find('strong', class_='value d-block lh-4 fs-4 fw-700').get_text().strip()
    lpa_div = soup.find('div', {'title': 'Indicar se a empresa é ou não lucrativa. Se este número estiver negativo, a empresa está com margens baixas, acumulando prejuízos.'})
    lpa = lpa_div.find('strong', class_='value d-block lh-4 fs-4 fw-700').get_text().strip()

    # Calculating intrinsic and opportunity values
    intrinsic_value = intrinsic_value_calculous(lpa, vpa)
    oportunity_value = oportunity_value_calculous(intrinsic_value, actual_value)

    # Storing the data in a dictionary
    data = {"Stock": stock,
            "Value": actual_value,
            "DY": dividend_yield,
            "VPA": vpa,
            "LPA": lpa,
            "Intrinsic Value": intrinsic_value,
            "Oportunity Value": oportunity_value
            }

    # Appending the dictionary to the list
    dictionary_data.append(data)

# Looping through the list of stocks and calling the function to get indicators
for stock in list_stocks:
    get_indicators(stock)

# Creating a DataFrame from the list of dictionaries
df = pd.DataFrame(dictionary_data)

# Formatting columns in the DataFrame
df['LPA'] = df['LPA'].apply(format_percentage)
df['VPA'] = df['VPA'].apply(format_percentage)
df['DY'] = df['DY'].apply(format_percentage)
df['Value'] = df['Value'].apply(format_money)
df['Intrinsic Value'] = df['Intrinsic Value'].apply(format_money)
df['Oportunity Value'] = df['Oportunity Value'].apply(format_percentage)

# Printing the final DataFrame
print(df)
