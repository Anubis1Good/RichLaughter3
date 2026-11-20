from cscalp_client import CscalpClient

client = CscalpClient("http://localhost:7777")

# 1. При старте ждем готовности счетов и подписываемся на нужные бумаги
client.wait_until_ready(["LiteInvest:stock", "LiteInvest:fut"])
client.subscribe("LiteInvest:stock", ["TATN", "SBER", "APTK"])

# 2. Внутри торгового цикла:
df = client.get_candles("LiteInvest:stock", "TATN", tf_minutes=5, limit=200)
pos = client.get_position("LiteInvest:stock", "TATN")
orders = client.get_orders("LiteInvest:stock", "TATN")

# Стратегия выдает абстрактный сигнал ("BUY", "SELL", "HOLD")
signal = "BUY"

# Слой контроля позиций решает, исполнять ли сигнал:
if signal == "BUY" and pos["amount"] == 0 and len(orders["limitOrders"]) == 0:
    # Встаем лучшим покупателем в стакан на 1 лот
    client.buy_limit("LiteInvest:stock", "TATN", amount=1, price=None)
