import hmac
import time
from hashlib import sha256
from urllib.parse import urlencode

import requests  # pip install requests

API_URL = "https://paxful.com/api/"
API_KEY = "i1BYYkOJ4bQhsNPovtlFYIviGrjfmMiM"
API_SECRET = "K06b3b9c0WjaNWdJ2aQ2F0n3Mqc5Imye"

class PaxfulBot():
    def __init__(self, data):
        print('Bot start!')
        self.setBot(data['job_settings'])
    
    def __del__(self):
        print("Bot stop !")
    
    def setBot(self, settings):
        print(settings)
        self.monitoringGaps = settings['monitoringgaps']
        self.messages = settings['messages']
        self.activedtrades = list()

    def callapis(self, url, params=''):
        nonce = int(time.time())
        payload = {"apikey": API_KEY, "nonce": nonce}
        payload = urlencode(sorted(payload.items()))
        apiseal = hmac.new(API_SECRET.encode(), payload.encode(), sha256).hexdigest()
        data_with_apiseal = payload + "&apiseal=" + apiseal
        headers = {"Accept": "application/json", "Content-Type": "text/plain"}
        resp = requests.post(url, data=data_with_apiseal, headers=headers)
        print(resp)
        return resp

    def getTradeList(self):
        url = API_URL + 'trade/list'
        return self.callapis(url)
    
    def getTradeChatLatest(self, trade_hash):
        url = API_URL + 'trade-chat/latest'
        return self.callapis(url)
    
    def run(self):

        while True:
            self.activedtrades = self.getTradeList()
            for trade in self.activedtrades:
                trade_hash = trade


            sleep(self.monitoringGaps)

def main():
    with open('PaxfulBotSetting.json') as json_file:
        print('loaded config.json file')
        data = json.load(json_file)
        my_bot = PaxfulBot(data)
        my_bot.run()

if __name__ == '__main__':
    main()
