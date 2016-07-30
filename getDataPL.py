import requests, cPickle, shutil, time

all = {}
errorout = open('errors.log', 'w')

date_text = time.strftime("%Y_%m_%d")

all_data_url = 'https://fantasy.premierleague.com/drf/elements/'
r_all = requests.get(all_data_url)
all_data = r_all.json()

for i in range(490): #486
    playerurl = 'https://fantasy.premierleague.com/drf/element-summary/%s'
    r = requests.get(playerurl % i)

    # skip non-existent players
    if r.status_code != 200: continue
    
    temp = r.json()
    all_data[i-1]['history_past'] = temp['history_past']

print date_text

cPickle.dump(all_data, open(date_text + '_all_data.p','wb'))
