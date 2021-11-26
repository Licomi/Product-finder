from bs4 import BeautifulSoup
import requests, sqlite3, re


# headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36'}
# soup = BeautifulSoup(requests.get('https://www.ozon.ru', headers=headers).text, 'lxml')https://www.wildberries.ru/
soup = BeautifulSoup(requests.get('https://www.wildberries.ru/', headers=headers).text, 'lxml')
list_a_soup = soup.find_all('a', {'href': re.compile('cat')} )

for i in list_a_soup:
    print(i)

print(len(list_a_soup))