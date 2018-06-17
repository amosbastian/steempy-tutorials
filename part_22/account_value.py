from steem.account import Account
from steem.amount import Amount
from steem import Steem

import json, sys, requests

def get_market_price(token):
    api_url = 'https://api.coinmarketcap.com/v1/ticker/{}/'.format(token)
    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))[0]['price_usd']
    else:
        return None

steem = float(get_market_price('steem'))
sbd = float(get_market_price('steem-dollars'))

print ("Steem/USD: {:.2f}\nSBD/USD: {:.2f}\n".format(steem, sbd))

username = sys.argv[1]
stats = {}

nodes = ['https://rpc.buildteam.io', 'https://api.steemit.com']
s = Steem(nodes)

data = s.get_dynamic_global_properties()
total_vesting_shares = Amount(data["total_vesting_shares"]).amount
total_vesting_fund_steem = Amount(data["total_vesting_fund_steem"]).amount
ratio = total_vesting_fund_steem/total_vesting_shares

account = Account(str(username), s)
for key, value in account.get_balances()['total'].items():
    if key not in stats:
        stats[key] = value

liquid_steem = stats['STEEM']
liquid_sbd = stats['SBD']
vested_steem = stats['VESTS']*ratio

print ("Steem: {:.3f}".format(liquid_steem))
print ("SBD: {:.3f}".format(liquid_sbd))
print ("Steem Power: {:.3f}".format(vested_steem))
print ()
print ("Dollar value: {:.2f}".format(liquid_steem*steem+liquid_sbd*sbd+vested_steem*steem))
