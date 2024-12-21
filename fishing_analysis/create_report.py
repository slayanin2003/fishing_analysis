from pathlib import Path
import re

import numpy as np
import pandas as pd
from pandas import DataFrame

from fishing_analysis.types_module import UserRequest, UserFishingStats, RequestCounter
import matplotlib.pyplot as plt


def _create_users_list(requests: list[UserRequest]) -> list[UserFishingStats]:
    user_stats = []
    for request in requests:
        user_stats.append(UserFishingStats(request.ip, 0))
    return user_stats


def _count_requests(requests: list[UserRequest]) -> list[RequestCounter]:
    request_count = []
    for request in requests:
        request_count.append(RequestCounter(request.url, 0))

    for req in request_count:
        for request in requests:
            if req.url == request.url:
                req.count_request += 1

    request_count.sort(key=lambda x: x.count_request, reverse=True)
    return request_count


def make_pie_graph(requests: list[UserRequest], root_dir: Path) -> Path:
    count_fishing = 0
    count_legit = 0
    for request in requests:
        if request.valid == 0:
            count_fishing += 1
        else:
            count_legit += 1

    values = [count_legit, count_fishing]
    labels = ['Легитимные запросы', 'Фишинговые запросы']
    plt_path = root_dir / 'files' / 'graphics' / 'requests_stats.png'
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['#12329e', '#9e1212'])
    plt.savefig(plt_path.as_posix())
    plt.close()
    return plt_path


def make_users_stats_graph(requests: list[UserRequest], root_dir: Path) -> Path:
    user_request_stats = _create_users_list(requests)
    for user in user_request_stats:
        for user_request in requests:
            if user.ip == user_request.ip and user_request.valid == 1:
                user.count_fishing_requests += 1

    user_request_stats.sort(key=lambda x: x.count_fishing_requests)
    values: list[int] = []
    users = []
    for user in user_request_stats:
        values.append(user.count_fishing_requests)
        users.append(user.ip)

    plt_path = root_dir / 'files' / 'graphics' / 'user_stats.png'
    colors = plt.cm.Reds(np.linspace(0.5, 1, len(values)))
    plt.figure(figsize=(12, 3))
    plt.barh(users, values, color=colors)
    plt.savefig(plt_path)
    plt.close()
    return plt_path


def _percent_to_values(percent: float, all_values: list[int]) -> str:

    absolute = round(percent * sum(all_values) / 100)
    return f'{absolute}'


def make_stats_of_popular_requests(requests: list[UserRequest], root_dir: Path) -> Path:
    request_counter = _count_requests(requests)
    urls = []
    urls_count = []
    for req in request_counter:
        urls.append(req.url)
        urls_count.append(req.count_request)

    plt_path = root_dir / 'files' / 'graphics' / 'requests_popular.png'
    plt.figure(figsize=(12, 8))
    plt.pie(urls_count[:10], labels=urls[:10], autopct=lambda pct: _percent_to_values(pct, urls_count[:10]))
    plt.savefig(plt_path.as_posix())
    plt.close()
    return plt_path


IP_ADDRESS = r'^((25[0-5]|2[0-4]\d|1?\d\d?)\.){3}(25[0-5]|2[0-4]\d|1?\d\d?)$'


def make_stats_of_user_requests(siem_data: DataFrame, user_ip: str) -> DataFrame:
    if not re.match(IP_ADDRESS, user_ip):
        error_df = pd.DataFrame(columns=['SourceIP', 'InvalidIP'])
        error_df.loc[0] = [user_ip, 'Некорректный формат IPv4']
        return error_df

    user_data = siem_data[siem_data['SourceIP'] == user_ip]
    if user_data.shape[0] == 0:
        user_data = pd.DataFrame(columns=['SourceIP', 'NoIPInData'])
        user_data.loc[0] = [user_ip, 'Нет информации по данному IP адресу']
        return user_data

    return user_data
