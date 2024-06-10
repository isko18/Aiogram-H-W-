from config import token
import schedule
import time
import requests
def test():
    print("hello geeks")
    print(time.ctime())

def get_btc_price():
    print('----btc----')
    url = f"https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    responce = requests.get(url=url).json()
    price = responce.get('price')
    print(f'{time.ctime()},{price}$')
    
    
    
# schedule.every(2).seconds.do(test)
# schedule.every(1).minutes.do(test)
# schedule.every(1).day.at("17:32").do(test)
# schedule.every(1).thursday.at("17:32","Asia/Astana").do(test)
# schedule.every(1).day.at("17:32","Asia/Astana").do(test)
# schedule.every().hour.at(":32").do(test)
schedule.every(1).seconds.do(get_btc_price)
    
while True:
    schedule.run_pending()
    


