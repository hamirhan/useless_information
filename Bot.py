import telebot
import datetime
import pytz
import threading
import time
import wikipediaapi
import random
import pyowm
import shelve
from PIL import Image

users = {}
users_inf_len = 3
with shelve.open('useless_log') as logger:
    for j in logger:
        users[int(j)] = logger[j]


def saver():
    while True:
        with shelve.open('useless_log') as log:
            for u in users:
                log[str(u)] = users[u]
        time.sleep(10)


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
    rand_lat = round(rand_lat, 5)
    rand_lon = round(rand_lon, 5)
    observation = mgr.weather_at_coords(rand_lat, rand_lon)
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
    temp_sum = round(temp_sum, 2)
    information = f'сегодняшние случайные координаты: {rand_lat}, {rand_lon}\n'\
                  f'Давление там сейчас: {press} Гектопаскаль\n' \
                  f'А темепратура там: {temperature} Кельвина\n' \
                  f'Средняя температура на планете Земля: {temp_sum} Цельсия'
    return [information, rand_lat, rand_lon]


def generate_image():
    img = Image.new('RGB', (120, 120), color=(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)))
    img.save('random_color.png')


def historical_information():
    days = ["", "января", "февраля", "марта", "апреля", "мая", "июня",
            "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    a = datetime.datetime.now().astimezone(pytz.timezone('Europe/Moscow'))
    page_name = str(int(str(a)[8:10])) + ' ' + days[int(str(a)[5:7])]
    wiki = wikipediaapi.Wikipedia('ru')
    wp = wiki.page(page_name)
    d = wp.text
    f = 0
    g = 0
    while f < len(d) and d[f:f + 13] != 'До XVIII века'\
            and d[f:f + 11] != 'До XIX века' and d[f:f + 12] != 'До XVII века' and d[f:f + 7] != 'XIX век' and\
            d[f:f + 9] != 'XVIII век' and d[f:f + 8] != 'XVII век':
        f += 1
    while g < len(d) and d[g:g + 8] != 'Родились':
        g += 1
    lines_counter = 0
    h = f
    k = h
    lines = []
    while h < g:
        h = k
        while d[k] != '\n':
            k += 1
        k += 1
        lines.append(d[h:k])
        lines_counter += 1
    lines += ['']
    random_line = 0
    while not (lines[random_line][0].isdigit() and
               random_line + 1 != len(lines) and lines[random_line + 1][0].isdigit()):
        random_line = random.randint(0, lines_counter - 1)
    random_information = ''
    random_information += lines[random_line]
    s = 0
    while random_information[s].isdigit():
        s += 1
    ri = str(int(str(datetime.datetime.now())[:4]) - int(random_information[:s]))
    information = ''
    if int(ri) == 13 or int(ri) == 12 or int(ri) == 11:
        information += 'ровно '
        information += ri + ' '
        information += 'лет назад, в '
    elif ri[-1] == '1':
        information += 'ровно '
        information += ri + ' '
        information += 'год назад, в '
    elif ri[-1] == '2' or ri[-1] == '3' or ri[-1] == '4':
        information += 'ровно '
        information += ri + ' '
        information += 'года назад, в '
    else:
        information += 'ровно '
        information += ri + ' '
        information += 'лет назад, в '
    information += random_information
    return information


def false_maker(who):
    time.sleep(120)
    users[who][2] = False


def sender(who):
    bot.send_message(who, historical_information())
    geography = weather_information()
    bot.send_message(who, geography[0])
    bot.send_location(who, geography[1], geography[2])
    generate_image()
    bot.send_message(who, 'Ваш цвет дня:')
    bot.send_photo(who, open('random_color.png', 'rb'))


def check_time():
    global users
    while True:
        time.sleep(40)
        for u in users:
            if len(users[u]) < users_inf_len:
                users[u] = users[u] + [False]
            if str(datetime.datetime.now().astimezone(pytz.timezone('Europe/Moscow')).time())[:5] == users[u][0]\
                    and not users[u][2]:
                users[u][2] = True
                threading.Thread(target=lambda: false_maker(u)).start()
                threading.Thread(target=lambda: sender(u)).start()


def check_if_time(text):
    if len(text) == 5 and text[0].isdigit() and text[1].isdigit() and \
        text[2] == ':' and text[3].isdigit() and text[4].isdigit() and 0 <= int(text[:2]) < 24 and \
       0 <= int(text[3:5]) < 60:
        return True
    else:
        return False


bot = telebot.TeleBot('875049280:AAFwnzJknMiUwypR63W6TQ6Xvj0nRhmp1PQ')
threading.Thread(target=check_time).start()
threading.Thread(target=saver).start()


@bot.message_handler(commands=['start'])
def starter(message):
    global users
    if message.from_user.id in users:
        bot.send_message(message.from_user.id, f'you are already in, welcome back, you will receive message at '
                                               f' {users[message.from_user.id][0]}')
    else:
        bot.send_message(message.from_user.id, 'Welcome. It is useless bot and it will send you some random'
                                               ' information every day whenever you want,'
                                               ' just send command /change_time (you will get messages at 9:00 am until'
                                               ' you change it)')
        users[message.from_user.id] = ['09:00', 'none', False]


@bot.message_handler(commands=['change_time'])
def change_time(message):
    global users
    users[message.from_user.id][1] = 'time'
    bot.send_message(message.from_user.id, 'tell me when you want to get your portion of information (hh:mm)')


@bot.message_handler(commands=['send_now'])
def send_now(message):
    threading.Thread(target=lambda: sender(message.from_user.id)).start()


@bot.message_handler(content_types=['text'])
def distributor(message):
    if users[message.from_user.id][1] == 'time':
        if check_if_time(message.text):
            users[message.from_user.id][0] = message.text
            bot.send_message(message.from_user.id, f'time set for {users[message.from_user.id][0]}')
        else:
            bot.send_message(message.from_user.id, 'wrong time')


bot.polling()
