import hmac
from hashlib import sha256
from urllib.parse import urlencode
import json
from time import sleep,time
from datetime import datetime

import requests  # pip install requests

API_URL = "https://paxful.com/api/"
API_KEY = ""
API_SECRET = ""

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
        self.setHashs = set()
        self.author = 'smeago'

    def callapis(self, url, params=''):
        try:
            nonce = int(time())
            payload = {"apikey": API_KEY, "nonce": nonce}
            payload = urlencode(sorted(payload.items()))
            apiseal = hmac.new(API_SECRET.encode(), payload.encode(), sha256).hexdigest()
            data_with_apiseal = payload + "&apiseal=" + apiseal
            headers = {"Accept": "application/json", "Content-Type": "text/plain"}
            resp = requests.post(url, data=data_with_apiseal, headers=headers)
        except:
            return 0
        # print(resp)
        return resp

    def getTradeList(self):
        url = API_URL + 'trade/list'
        return self.callapis(url)
    
    def getTradeChatLatest(self):
        url = API_URL + 'trade-chat/latest'
        response = self.callapis(url)
        # if response.text
        return response
    def postTradeChat(self, trade_hash):
        url = API_URL + 'trade-chat/post'
        nonce = int(time())
        payload = {"apikey": API_KEY, "nonce": nonce, "trade_hash": trade_hash, "message": '\n'.join(map(str, self.messages)).replace(' ','%20')}
        payload = urlencode(sorted(payload.items()))
        apiseal = hmac.new(API_SECRET.encode(), payload.encode(), sha256).hexdigest()
        data_with_apiseal = payload + "&apiseal=" + apiseal
        headers = {"Accept": "application/json", "Content-Type": "text/plain"}
        resp = requests.post(url, data=data_with_apiseal, headers=headers)
        # print(json.loads(resp.text['data']))
        return resp
        # return self.callapis(url, trade_hash)
    
    def run(self):
        # changed_send = False
        # if changed_send:
        self.activedtrades = self.getTradeChatLatest()
        if self.activedtrades != 0:
            try:
                self.msgLists = json.loads(self.activedtrades.text)['data']['trades']
                for trade_hash in self.msgLists:

                    for msg in self.msgLists[trade_hash]['messages']:
                        if msg['author'] == self.author and self.messages[0] in msg['text']:
                            self.setHashs.add(trade_hash)

                    # # trade_hash = msg.key()
                    # if not trade_hash in self.setHashs:
                        
                    # else:
                    #     pass 
            except:
                pass
        else:
            pass
        while True:
            self.activedtrades = self.getTradeChatLatest()
            # print(self.activedtrades)
            # self.tradeList = self.getTradeList()
            # print(self.tradeList)
            if self.activedtrades != 0:
                self.msgLists = json.loads(self.activedtrades.text)['data']['trades']
                print('current activated trades: ', len(self.msgLists))
                for trade_hash in self.msgLists:
                    print('current trade hash: ', trade_hash)
                    # trade_hash = msg.key()
                    if not trade_hash in self.setHashs:
                        for msg in self.msgLists[trade_hash]['messages']:
                            if msg['author'] != None and msg['author'] != self.author:
                                print('I sent a message to the trader with trade hash: ', trade_hash)
                                self.postTradeChat(trade_hash)
                                self.setHashs.add(trade_hash)
                                print('current sent trade hash set count: ', len(self.setHashs))
                                break
                            else:
                                continue
                    else:
                        pass 
                    sleep(3)
                self.setHashs = set(self.msgLists)
                now = datetime.now()
                # dd/mm/YY H:M:S
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                print("current date and time =", dt_string)
                print('sleeping seconds: ', self.monitoringGaps)
                sleep(self.monitoringGaps)

def main():
    with open('PaxfulBotSetting.json') as json_file:
        print('loaded config.json file')
        data = json.load(json_file)
        my_bot = PaxfulBot(data)
        while True:
            print('bot running :')
            my_bot.run()
            sleep(3)

if __name__ == '__main__':
    main()
