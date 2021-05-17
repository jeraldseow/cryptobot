import websocket, json, pprint, talib, numpy, sender

ETH_USDT = "ethusdt"
BTC_USDT = "btcusdt"

SOCKET = f"wss://stream.binance.com:9443/ws/{BTC_USDT}@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSD"


closes = []

def on_open(ws):
    print("Opened Connection")

def on_close(ws):
    print("Closed Connection")

def on_message(ws, message):
    global closes

    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if True: #change to if is_candle_closed, now true for testing purposes
        print("candle closed at {}".format(close))
        closes.append(float(close))
        #sender.send_message(f"Current Etherium price: {close}")
        
        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            last_rsi = rsi[-1]
            print("the latest RSI is {}".format(last_rsi))
            closes.pop(0)
            print("Closes:")
            print(closes)

            if last_rsi > RSI_OVERBOUGHT:
                print("SELL - BEING OVERBOUGHT")
                sender.send_message(f"Etherium being overbought, current price: {close}. Can consider selling!")

            if last_rsi < RSI_OVERSOLD:
                print("BUY - BEING OVERSOLD")
                sender.send_message(f"Etherium being oversold, current price: {close}. Can consider buying!")

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()