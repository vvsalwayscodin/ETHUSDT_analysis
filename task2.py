import ccxt
import pandas as pd
import time

exchange = ccxt.binance({'rateLimit': 2000, 'enableRateLimit': True})
symbol = 'ETH/USDT'

# Создаем пустой DataFrame для хранения данных о цене
price_history = pd.DataFrame(columns=['timestamp', 'price'])

# Основной цикл программы
while True:
    # Получаем актуальную цену
    ticker = exchange.fetch_ticker(symbol)
    price = ticker['last']
    timestamp = pd.Timestamp.now()

    # Добавляем новую строку в DataFrame
    price_history = price_history.append({'timestamp': timestamp, 'price': price}, ignore_index=True)

    # Вычисляем изменение цены за последний час
    last_hour_prices = price_history[price_history['timestamp'] >= timestamp - pd.Timedelta(hours=1)]
    price_change = (price - last_hour_prices.iloc[0]['price']) / last_hour_prices.iloc[0]['price']

    # Если изменение цены превышает 1%, выводим сообщение в консоль
    if abs(price_change) > 0.01:
        print(f"Price change in the last hour: {price_change:.2%}")

    # Ждем 10 секунд перед следующим запросом к API
    time.sleep(10)
