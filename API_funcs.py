import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import uuid
import numpy as np

from APIGen import getAPIKey
from settings import username, password


# Функция для формирования CSV-файла
def get_data(lat1, lon1, lat2, lon2, user_id, side=.02) -> int:
    language = 'ru'
    format = 'json'
    function = 'box'

    latMin, latMax = sorted([lat1, lat2])
    lonMin, lonMax = sorted([lon1, lon2])

    latSpace = np.linspace(latMin, latMax, max(2, round(abs(latMax - latMin) / side + .5)), endpoint=True)
    lonSpace = np.linspace(lonMin, lonMax, max(2, round(abs(lonMax - lonMin) / side + .5)), endpoint=True)
    keysNeed = len(latSpace) * len(lonSpace)
    keys = getAPIKey(username, password, keysNeed)


    pageNum = 1
    ID, TITLE, URL, LOC = [[] for _ in range(4)]
    DESC, PHOTO = [], []

    while True:
        for lat in range(len(latSpace) - 1):
            for lon in range(len(lonSpace) - 1):

                key = lat + lon
                resp = \
                    f'https://api.wikimapia.org/?key={keys[key % len(keys)]}&function={function}&format={format}&language={language}&lon_min={lonSpace[lon]}&lat_min={latSpace[lat]}&lon_max={lonSpace[lon + 1]}&lat_max={latSpace[lat + 1]}&count=100&page={pageNum}'

                try:
                    response = requests.get(resp)
                    resJSON = json.loads(response.text)
                    objects = resJSON["folder"]

                    if objects:
                        for obj in objects:
                            if obj['id'] not in ID:
                                ID.append(obj['id'])
                                TITLE.append(obj['name'])
                                URL.append(obj['url'])
                                LOC.append(obj['location'])

                                page = requests.get(obj['url'], headers={
                                    'User-agent': str(uuid.uuid1()) + ' BOT'})
                                if page.status_code == 200:
                                    soup = BeautifulSoup(page.text, "html.parser")
                                    allPics = [img['src'] for img in soup.findAll('img', class_='photo-thumbnail')]
                                    PHOTO.append(allPics)

                                    soup = BeautifulSoup(page.text, "html.parser")
                                    remove_attr = ['<br/>', '<div class="placeinfo-row" id="place-description">',
                                                   '</div>',
                                                   'rel="nofollow"', 'target="_blank"']
                                    desc = soup.findAll('div', {"id": "place-description"})
                                    desc = str(desc[0] if desc else '-')

                                    for attr in remove_attr:
                                        desc = desc.replace(attr, '')
                                    DESC.append(desc)

                        pageNum += 1
                    else:
                        break
                except Exception:
                    break
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

    dataFrame.to_csv(f'{user_id}_output.csv', encoding='utf-8', index=False)

    return len(dataFrame)
