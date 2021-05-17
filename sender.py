import requests, constants

TOKEN = constants.TELEGRAM_TOKEN

USER = constants.bitcoin_babies

def send_message(text):
    global TOKEN, USER
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={USER}&text={text}"
    work = requests.get(url)