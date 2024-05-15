import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import string
import random

letters = string.ascii_lowercase


# Функция для формирования CSV-файла
def get_data(lat1, lon1, lat2, lon2) -> int:
    key = 'example',
    language = 'ru'
    format = 'json'
    function = 'box'

    latMin, latMax = sorted([lat1, lat2])
    lonMin, lonMax = sorted([lon1, lon2])

    pageNum = 1
    ID, TITLE, URL, LOC = [[] for _ in range(4)]
    DESC, PHOTO = [], []

    while True:
        resp = f'https://api.wikimapia.org/?key={key[0]}&function={function}&format={format}&language={language}&lon_min={lonMin}&lat_min={latMin}&lon_max={lonMax}&lat_max={latMax}&count=100&page={pageNum}'

        response = requests.get(resp)
        resJSON = json.loads(response.text)
        objects = resJSON["folder"]

        if objects:
            for obj in objects:
                ID.append(obj['id'])
                TITLE.append(obj['name'])
                URL.append(obj['url'])
                LOC.append(obj['location'])

                page = requests.get(obj['url'], headers={
                    'User-agent': ''.join(random.choice(letters) for _ in range(random.randint(5, 15))) + ' BOT'})
                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    allPics = [img['src'] for img in soup.findAll('img', class_='photo-thumbnail')]
                    PHOTO.append(allPics)

                    soup = BeautifulSoup(page.text, "html.parser")
                    remove_attr = ['<br/>', '<div class="placeinfo-row" id="place-description">', '<div/>',
                                   'rel="nofollow"', 'target="_blank"']
                    desc = soup.findAll('div', {"id": "place-description"})
                    desc = str(desc[0] if desc else '-')

                    for attr in remove_attr:
                        desc = desc.replace(attr, '')
                    DESC.append(desc)

            pageNum += 1
        else:
            break

    dataFrame = pd.DataFrame(
        data={
            'id': ID,
            'Название': TITLE,
            'Ссылка': URL,
            'Расположение': LOC,
            'Описание': DESC,
            'Фото': PHOTO
        }
    )

    dataFrame.to_csv('output.csv', encoding='utf-8', index=False)

    return len(dataFrame)
