from bs4 import BeautifulSoup
import requests
from Queue import Queue

url = 'https://baike.baidu.com/item/%E7%99%BE%E7%A7%91'
q = Queue()

html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
bs = BeautifulSoup(html.content,'html.parser')
for item in bs.find_all('img'):
    print (item)
    q.put(item)

while q.not_empty:
    print(q.get()['src'])