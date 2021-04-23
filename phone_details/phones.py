import json
import requests
from bs4 import BeautifulSoup

GSM_ARENA = 'https://www.gsmarena.com/'
GSM_ARENA_BRANDS = GSM_ARENA + 'makers.php3' # all brands

def fetch_data(url, classes, lists, base_url=None, limit=1):
    '''
    Fetches data about phones from a url (gsmarena homepage or brand list).

    Requires:
        - url (str): url from where to gather information.
        - classes (str): class from container div element to select.
        - lists (str): html list element to select.
        - base_url (str - optional): homepage url.
        - limit (int - optional): maximum number of phones per brand).
    Ensures:
        - data.json (file): Saves a json file with phone brand and model, and
          gsmarena link with details, for each phone.
    '''
    if base_url is None:
        base_url = url

    data = {}

    # Find each brand
    page_source = requests.get(url)
    html = page_source.text
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('div', class_=classes):
        for i, li in enumerate(link.find_all(lists), 1):
            for anchor in li.find_all('a'):
                anchor_href = base_url + anchor.get('href')
                brand = anchor.contents[0]
                print()
                print(i, brand, anchor_href)

                # Find each model
                page_source = requests.get(anchor_href)
                html = page_source.text
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('div', class_='makers'):
                    list_items = link.find_all('a')

                    num_items = len(list_items)
                    if limit is None or num_items < limit:
                        limit = num_items

                    for i, anchor in enumerate(list_items[:limit]):
                        anchor_href = base_url + anchor.get('href')
                        item_name = anchor.find('span').get_text(" ")

                        data[item_name] = anchor_href
                        print("\t", i, brand, item_name, "-", anchor_href)

    with open('data.json', 'w') as f:
        json.dump(data, f)


# Example usage:
# fetch_data(GSM_ARENA_BRANDS, 'st-text', 'td', GSM_ARENA, 5) # all brands
# fetch_data(GSM_ARENA, 'brandmenu-v2 light l-box clearfix', 'li') # main brands
