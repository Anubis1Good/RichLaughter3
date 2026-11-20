import time
import requests

BASE = "http://localhost:7777"
SLOT = "LiteInvest:stockLI"
TICKER = "APTK"

# 1. Подписываемся на APTK
sub = requests.post(f"{BASE}/subscribe", json={"slot": SLOT, "tickers": [TICKER]}).json()
print("Подписка:", sub)

# Даем 1 секунду на прохождение репликаций и получение стакана
time.sleep(1.5)

# 2. Получаем лучшие цены и шаг цены инструмента
bp = requests.get(f"{BASE}/best-prices", params={"slot": SLOT, "ticker": TICKER}).json()
print("Лучшие цены:", bp)

step = bp["step"]
decimals = bp["decimals"]
safe_buy_price = round(bp["bestBid"] - (step * 10), decimals)
print(f"Расчетная безопасная цена покупки (-10 шагов): {safe_buy_price}")

# 3. Выставляем лимитную заявку (1 лот)
order_res = requests.post(f"{BASE}/order", json={
    "slot": SLOT,
    "ticker": TICKER,
    "side": "BUY",
    "amount": 1,
    "price": safe_buy_price
}).json()
print("Результат отправки заявки:", order_res)

time.sleep(1)

# 4. Проверяем список активных заявок
orders = requests.get(f"{BASE}/orders", params={"slot": SLOT, "ticker": TICKER}).json()
print("Активные заявки на бирже:", orders)

# 5. Ждем 3 секунды и снимаем заявку
# time.sleep(3)
# cancel_res = requests.post(f"{BASE}/cancel", json={
#     "slot": SLOT,
#     "ticker": TICKER
# }).json()
# print("Результат снятия:", cancel_res)

time.sleep(1)
print("Заявки после снятия:", requests.get(f"{BASE}/orders", params={"slot": SLOT, "ticker": TICKER}).json())

