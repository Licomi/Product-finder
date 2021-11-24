from sqlite3.dbapi2 import Binary
from bs4 import BeautifulSoup
import requests, sqlite3, re


def get_icon_site(url: str) -> Binary:
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    icon_url = soup.find('link', {'rel': re.compile('icon')}).get('href')
    if icon_url[:2] == '//':
        icon_url = url[0:url.index('/')] + icon_url
    elif icon_url[0] == '/':
        icon_url = url + icon_url
    return requests.get(icon_url).content


URLS = ['https://aliexpress.ru/all-wholesale-products.html', 'https://www.ozon.ru', 'https://www.wildberries.ru', 'https://alexgyver.ru', 'https://arduino54.ru']
id_shop = 1


# Поиск категорий
soup = BeautifulSoup(requests.get(URLS[0]).text, 'lxml')

list_catigory_soup = soup.find_all('h3', {'class': 'big-title anchor1 anchor-agricuture'} )
list_sub_catigory_soup = soup.find_all('ul', {'class': 'sub-item-cont util-clearfix'})

lsit_shop_category = []
for i_category, category in enumerate(list_catigory_soup):
    list_sub_catigory = []
    for li in list_sub_catigory_soup[i_category]:
        if li.name != None:
            list_sub_catigory.append((li.a.text, 'https:' + li.a.get("href")))
    lsit_shop_category.append((category.a.text, 'https:' + category.a.get('href'), list_sub_catigory))


conn = sqlite3.connect('DATABASE.db')
cursor = conn.cursor()

for i_c, category in enumerate(lsit_shop_category):
    cursor.execute(""" INSERT INTO Сategories(id_shop, name, url)
                      VALUES(?, ?, ?)""", (id_shop, category[0], category[1]))
    cursor.execute("""SELECT * FROM Сategories""")
for i in cursor.fetchall():
    print(i)
conn.commit()
    # print(i_c, category[0], category[1])
    # print(category[2])
    # if i_c == 1: break
