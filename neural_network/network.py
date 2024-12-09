import pickle
import re
from pathlib import Path
import numpy as np


def extract_features(url):
    # Проверяет, содержит ли URL IP-адрес (например, "192.168.0.1")
    def has_ip_address(url):
        return int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)))

    # Проверяет, содержит ли URL символ "@"
    def has_at_symbol(url):
        return int('@' in url)

    # Возвращает длину URL
    def get_url_length(url):
        return len(url)

    # Вычисляет глубину URL (количество "/" в пути URL)
    def get_url_depth(url):
        return url.count('/')

    # Проверяет наличие перенаправления ("//") после протокола (например, "http://example.com//path")
    def has_redirection(url):
        return int('//' in url[7:])  # Пропускаем первые 7 символов ("http://")

    # Проверяет, начинается ли URL с "https" (указывает на защищённый протокол)
    def has_https_in_domain(url):
        return int(url.startswith('https'))

    # Проверяет, является ли URL сокращённым с помощью популярных сервисов
    def is_shortened_url(url):
        shorteners = [
            'bit.ly', 'tinyurl.com', 'goo.gl', 'shorte.st', 'x.co',
            'ow.ly', 'is.gd', 'buff.ly', 'adf.ly', 'go2l.ink', 't.co',
            'tr.im', 'cli.gs', 'yfrog.com', 'migre.me', 'ff.im',
            'tiny.cc', 'url4.eu', 'twit.ac', 'su.pr', 'twurl.nl',
            'snipurl.com', 'short.to', 'BudURL.com', 'ping.fm',
            'post.ly', 'Just.as', 'bkite.com', 'snipr.com', 'fic.kr',
            'loopt.us', 'doiop.com', 'short.ie', 'kl.am', 'wp.me',
            'rubyurl.com', 'om.ly', 'to.ly', 'bit.do', 'lnkd.in',
            'db.tt', 'qr.ae', 'cur.lv', 'ity.im', 'q.gs', 'po.st',
            'bc.vc', 'twitthis.com', 'u.to', 'j.mp', 'buzurl.com',
            'cutt.us', 'u.bb', 'yourls.org', 'prettylinkpro.com',
            'scrnch.me', 'filoops.info', 'vzturl.com', 'qr.net',
            '1url.com', 'tweez.me', 'v.gd', 'link.zip.net'
        ]
        return int(any(shortener in url for shortener in shorteners))

    # Проверяет, содержит ли домен URL дефис ("-")
    def has_hyphen_in_domain(url):
        domain = re.findall(r'://([^/]+)/?', url)[0] if '://' in url else url
        return int('-' in domain)

    # Собирает все признаки в виде списка
    return [
        has_ip_address(url),  # Признак наличия IP-адреса
        has_at_symbol(url),   # Признак наличия символа "@"
        get_url_length(url),  # Длина URL
        get_url_depth(url),   # Глубина URL
        has_redirection(url), # Признак перенаправления
        has_https_in_domain(url),  # Использование HTTPS
        is_shortened_url(url),     # Использование сокращённых ссылок
        has_hyphen_in_domain(url), # Наличие дефиса в домене
    ]


def predict(url):

    path_to_model = Path("model.pickle.dat")

    # Загружаем обученную модель из файла
    with open(path_to_model.as_posix(), 'rb') as file:
        model = pickle.load(file)

    # Извлекаем признаки из введённого URL
    features = extract_features(url)

    # Преобразуем признаки в массив и изменяем форму для модели
    input_array = np.array(features).reshape(1, -1)

    # Делаем предсказание с помощью модели
    prediction = model.predict(input_array)

    # Классы, возвращаемые моделью
    class_labels = ["Легитимный", "Фишинговый"]
    return class_labels[int(prediction[0])]
