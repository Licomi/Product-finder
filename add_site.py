from bs4 import BeautifulSoup
import requests, sqlite3, re, datetime
# import SQL_query


def get_icon_site(url: str) -> str:
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    icon_url = soup.find('link', {'rel': re.compile('icon')}).get('href')
    if icon_url[:2] == '//':
        icon_url = url[0:url.index('/')] + icon_url
    elif icon_url[0] == '/':
        icon_url = url + icon_url
    return requests.get(icon_url).content


def add_categories(DB_name: str, list_category, id_shop, show_result: bool = True) -> None:
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()

    for i_c, category in enumerate(list_category):
        cursor.execute(""" INSERT INTO Categories(id_shop, name, url)
                        VALUES(?, ?, ?)""", (id_shop, category[0], category[1]))
        for sub_category in category[2]:
            cursor.execute(""" INSERT INTO Sub_categories(id_category, name, url)
                        VALUES(?, ?, ?)""", (i_c+1, sub_category[0], sub_category[1]))
    if show_result:
        cursor.execute("""SELECT c.id, sc.id, c.name, sc.name, sc.url 
                            FROM Categories c 
                            INNER JOIN Sub_categories sc 
                            ON c.id = sc.id_category""")
        for i in cursor.fetchall():
            print(i)

    conn.commit()
    conn.close()

def parse_category_AliExpress(url: str):
    # Поиск категорий AliExpress
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    list_catigory_soup = soup.find_all('h3', {'class': 'big-title anchor1 anchor-agricuture'} )
    list_sub_catigory_soup = soup.find_all('ul', {'class': 'sub-item-cont util-clearfix'})

    # Формирование списка категорий AliExpress
    lsit_shop_category = []
    for i_category, category in enumerate(list_catigory_soup):
        list_sub_catigory = []
        for li in list_sub_catigory_soup[i_category]:
            if li.name != None:
                list_sub_catigory.append((li.a.text, 'https:' + li.a.get("href")))
        lsit_shop_category.append((category.a.text, 'https:' + category.a.get('href'), list_sub_catigory))
    return(lsit_shop_category)


URLS = ['https://aliexpress.ru/all-wholesale-products.html', 'https://www.ozon.ru', 'https://www.wildberries.ru', 'https://alexgyver.ru', 'https://arduino54.ru']

def search_item_AliExpress(item: str, category: int = None, w_db: bool = False, mode: int = 0) -> list:
    item = '%20'.join(item.split(' '))
    soup = BeautifulSoup(requests.get('https://aliexpress.ru/wholesale?SearchText=' + item).text, 'lxml')
    count_items = soup.find_all('div', {'class': 'SearchProductFeed_HorizontalCard__card__102el SearchProductFeed_Preview__card__3zxie'})

    # Информация о продавце
    conn = sqlite3.connect("DATABASE.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT id_site FROM Sellers""")
    list_sellers = cursor.fetchall()
    
    for i in count_items:
        lsit_new_sellers = []
        a_seller = i.find('a', {'href': re.compile('//aliexpress.ru/store/')})
        id_site = a_seller.get('href').split('/')[-1]
        if id_site not in list_sellers:
            print('https:' + a_seller.get('href'))
            print(requests.get('https:' + a_seller.get('href')).text)
            break
            # s_soup = BeautifulSoup(requests.get('https:' + a_seller.get('href')).text, 'lxml')
            # for j in s_soup.find_all('span'):
            #     print(j.text)
            
            # list_sellers.append()


search_item_AliExpress('arduino nano')




    

    # print(i_c, category[0], category[1])
    # print(category[2])
    # if i_c == 1: break
