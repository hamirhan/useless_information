import pyowm
import random


def weather_information():
    weather = pyowm.OWM('573b431e7f0de2240149d309cd8ce260')
    mgr = weather.weather_manager()
    rand_lat = random.random() * 90
    rand_lon = random.random() * 180
    negative = random.randint(-1, 1)
    while negative == 0:
        negative = random.randint(-1, 1)
    rand_lat *= negative
    negative = random.randint(-1, 1)
    while negative == 0:
        negative = random.randint(-1, 1)
    rand_lon *= negative
    observation = mgr.weather_at_coords(rand_lat, rand_lon)
    rand_lat = 52.5340152
    rand_lon = 39.2100076
    press = observation.weather.pressure['press']
    temperature = observation.weather.temperature()['temp']
    cords = [[49.3497111, -105.7473933],
             [-13.2131610, -59.6564494],
             [14.658726, 23.864741],
             [28.198590, 75.544428],
             [-23.190170, 124.235832],
             [60.957476, 132.497552],
             [51.267155, 21.233812],
             [68.707528, 29.495530],
             [14.570425, -88.629463],
             [32.808322, 41.636816]]
    temp_n = len(cords)
    temp_sum = 0
    for g in cords:
        temp_sum += mgr.weather_at_coords(g[0], g[1]).weather.temperature('celsius')['temp']
    temp_sum /= temp_n
    information = f'сегодняшние случайные координаты: {rand_lat}, {rand_lon}\n'\
                  f'Давление там сейчас: {press} Гектопаскаль\n' \
                  f'А темепратура там: {temperature} Кельвина\n' \
                  f'Средняя температура на планете Земля: {temp_sum} Цельсия'
    return information
