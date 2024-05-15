import requests
import json
import pandas as pd


# Функция для формирования CSV-файла
def get_data(lat1, lon1, lat2, lon2) -> int:
    key = 'example',
    language = 'ru'
    format = 'json'
    function = 'box'

    latMin, latMax = sorted([lat1, lat2])
    lonMin, lonMax = sorted([lon1, lon2])

    page = 1
    ID, TITLE, URL, LOC = [[] for _ in range(4)]

    while True:
        resp = f'https://api.wikimapia.org/?key={key[0]}&function={function}&format={format}&language={language}&lon_min={lonMin}&lat_min={latMin}&lon_max={lonMax}&lat_max={latMax}&count=100&page={page}'

        response = requests.get(resp)
        resJSON = json.loads(response.text)
        objects = resJSON["folder"]

        if objects:
            for obj in objects:
                ID.append(obj['id'])
                TITLE.append(obj['name'])
                URL.append(obj['url'])
                LOC.append(obj['location'])
            page += 1
        else:
            break

    dataFrame = pd.DataFrame(
        data={
            'id': ID,
            'Название': TITLE,
            'Ссылка': URL,
            'Расположение': LOC
        }
    )

    dataFrame.to_csv('output.csv', encoding='utf-8', index=False)

    return len(dataFrame)
