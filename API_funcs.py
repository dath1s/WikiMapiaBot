from wikimapia_api import API
import numpy as np
from math import floor
import pandas as pd

# Настройки API
API.config = \
    {
        'key': '0838653D-6414A31B-CC5BB66E-6F261C45-B1DEDAB0-59F1237E-0ACEDCBE-FD5E8D3A',
        'delay': 500,
        'language': 'ru'
    }


# Функция для формирования CSV-файла
def get_data(lat1, lon1, lat2, lon2) -> int:
    # Сортировка координат для формирования максимально и минимальной пары
    latMin, latMax = sorted([lat1, lat2])
    lonMin, lonMax = sorted([lon1, lon2])

    # Множетсво уникальных мест на карте
    placesSet = set()

    # Деление области на более мелкие полигоны для поиска
    lonLinSpace = np.linspace(lonMin, lonMax, num=floor(lonMax * 1e3) - floor(lonMin * 1e3))
    latLinSpace = np.linspace(latMin, latMax, num=floor(latMax * 1e3) - floor(latMin * 1e3))

    # Поиск ближайших объектов в более мелких областях
    for lon in lonLinSpace:
        for lat in latLinSpace:
            places = API.places.nearest(lon, lat)

            for obj in places:
                # Проверка на удовлетворение условию по координатам
                if lonMin <= obj['location']['lon'] <= lonMax and latMin <= obj['location']['lat'] <= latMax:
                    placesSet.add(str(obj))

    # Формировние CSV-файла
    ID, TITLE, URL, LOC = [[] for _ in range(4)]

    for obj in placesSet:
        objDict = eval(obj)

        ID.append(objDict['id'])
        TITLE.append(objDict['title'])
        URL.append(objDict['url'])
        LOC.append(objDict['location'])

    dataFrame = pd.DataFrame(data={
        'id': ID,
        'Название': TITLE,
        'Ссылка': URL,
        'Расположение': LOC
    })

    dataFrame.to_csv('output.csv', encoding='utf-8', index=False)

    return len(placesSet)
