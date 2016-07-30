import requests, cPickle, shutil, time

all = {}
errorout = open('errors.log', 'w')

date_text = time.strftime("%Y_%m_%d")
for i in range(19675):
    playerurl = 'http://www.premierleague.com/players/%s/player/stats'
    r = requests.get(playerurl % i)

    # skip non-existent players
    if r.status_code != 200: continue

    n = i
    time.sleep(1)
print i

37605