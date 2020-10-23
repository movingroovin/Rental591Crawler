from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

filename = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
page = requests.get('https://www.ptt.cc/bbs/hotboards.html')
soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.prettify())

name = []
bname = soup.select('.board-name')
for n in bname:
    name.append(n.text)
# print(name)

pop=[]
popularity = soup.select('.board-nuser')
for p in popularity:
    pop.append(int(p.text))
# print(pop)

dict = {'name': name,
       'popularity': pop
       }
hotboards = pd.DataFrame(dict)

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(hotboards)

sum(pop)

hotboards.index.name = 'rank'

hotboards.to_csv(filename+'.csv')