import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time

# Константы для API
BASE_URL = 'https://api.coingecko.com/api/v3'

# Функция для получения текущих цен криптовалют
def get_crypto_prices(crypto_ids, vs_currency='usd'):
    url = f"{BASE_URL}/simple/price?ids={','.join(crypto_ids)}&vs_currencies={vs_currency}"
    response = requests.get(url)
    data = response.json()
    return {crypto_id: data[crypto_id][vs_currency] for crypto_id in crypto_ids}

# Функция для загрузки исторических данных
def get_historical_data(crypto_id, vs_currency='usd', days=365):
    url = f"{BASE_URL}/coins/{crypto_id}/market_chart?vs_currency={vs_currency}&days={days}"
    response = requests.get(url)
    data = response.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

# Функция для анализа портфеля
def calculate_portfolio_value(crypto_holdings, crypto_ids):
    prices = get_crypto_prices(crypto_ids)
    total_value = sum(crypto_holdings[crypto_id] * prices[crypto_id] for crypto_id in crypto_ids)
    return total_value

# Функция для отображения графика
def plot_crypto_price(crypto_id, days=365):
    df = get_historical_data(crypto_id, days)
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['price'], label=f'Price of {crypto_id}')
    plt.title(f'{crypto_id} Price in Last {days} Days')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Пример портфеля
    crypto_holdings = {
        'bitcoin': 0.5,
        'ethereum': 2.0,
        'litecoin': 10.0
    }

    # Получение списка криптовалют для анализа
    crypto_ids = list(crypto_holdings.keys())
    
    # Расчет общей стоимости портфеля
    total_value = calculate_portfolio_value(crypto_holdings, crypto_ids)
    print(f"Total portfolio value: ${total_value:.2f}")

    # Построение графиков для каждой криптовалюты
    for crypto_id in crypto_ids:
        plot_crypto_price(crypto_id)
