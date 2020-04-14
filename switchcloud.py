import json
import requests
import time
from twilio.rest import Client

# SETUP
t = 30
account_sid = 'AC2c454f09cc769d4448bfda3d1518dd7e'
auth_token = '89938d7550d2926028006e6c5d8de92a'

# PRODUCTS INFO
sku1 = '14339173'
sku2 = '13817626'
sku3 = '13817625'

endpoint = 'http://api.bestbuy.ca/availability/products?skus='

url1 = endpoint + sku1
purchase1 = 'https://www.bestbuy.ca/en-ca/product/' + sku1

url2 = endpoint + sku2
purchase2 = 'https://www.bestbuy.ca/en-ca/product/' + sku2

url3 = endpoint + sku3
purchase3 = 'https://www.bestbuy.ca/en-ca/product/' + sku3


def run():
    while True:
        que(url1)
        que(url2)
        que(url3)
        time.sleep(t)


def fin(err):
    client = Client(account_sid, auth_token)
    client.messages.create(
            body='PROGRAM STOPPED: ' + err,
            from_='+17784880707',
            to='+17789182800'
        )
    print(err)
    print('PROGRAM STOPPED')
    exit()


def que(url):
    r = requests.get(url)

    if r.text[3:7] != 'avai':
        print(url)
        fin(r.text)

    decoded = r.content.decode('utf-8-sig')
    data = json.loads(decoded)
    sku = data['availabilities'][0]['sku']
    avai = data['availabilities'][0]['shipping']['purchasable']

    if not avai and sku == sku1:
        print('1 no')
        return

    if not avai and sku == sku2:
        print('2 no')
        return

    if not avai and sku == sku3:
        print('3 no')
        return

    if avai and sku == sku1:
        client = Client(account_sid, auth_token)
        client.messages.create(
                body='MARIO STOCK! ' + purchase1,
                from_='+17784880707',
                to='+17789182800'
            )
        client.messages.create(
                body='ASK MIKE WHAT HAPPENED!',
                from_='+17784880707',
                to='+17789802577'
            )
        print('1 yes')
        fin('EXIT WITH MARIO')

    if avai and sku == sku2:
        client = Client(account_sid, auth_token)
        client.messages.create(
                body='GREY STOCK! ' + purchase2,
                from_='+17784880707',
                to='+17789182800'
            )
        client.messages.create(
                body='ASK MIKE WHAT HAPPENED!',
                from_='+17784880707',
                to='+17789802577'
            )
        print('2 yes')
        fin('EXIT WITH GREY')

    if avai and sku == sku3:
        client = Client(account_sid, auth_token)
        client.messages.create(
                body='R&B STOCK! ' + purchase3,
                from_='+17784880707',
                to='+17789182800'
            )
        client.messages.create(
                body='ASK MIKE WHAT HAPPENED!',
                from_='+17784880707',
                to='+17789802577'
            )
        print('3 yes')
        fin('EXIT WITH R&B')

    else:
        print('ERROR')
        print(url)
        fin('ERROR')


run()
