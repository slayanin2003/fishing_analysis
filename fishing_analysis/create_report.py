from pathlib import Path

from fishing_analysis.types_module import UserRequest, UserFishingStats
import matplotlib.pyplot as plt
from fishing_analysis.__main__ import root_dir


def _create_users_list(requests: list[UserRequest]) -> list[UserFishingStats]:
    user_stats = []
    for request in requests:
        user_stats.append(UserFishingStats(request.ip, 0))
    return user_stats


def make_pie_graph(requests: list[UserRequest]) -> None:
    count_fishing = 0
    count_legit = 0
    for request in requests:
        if request.valid == 0:
            count_fishing += 1
        else:
            count_legit += 1

    values = [count_legit, count_fishing]
    labels = ['Легитимный', 'Фишинговый']
    plt.pie(values, labels=labels, autopct='%1.1f%%')

    plt_path = root_dir / 'graphics' / "Статистика запросов.png"
    plt.savefig(plt_path)
    return plt_path


def make_users_stats_graph(requests: list[UserRequest]) -> Path:
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

    plt.barh(users, values)
    plt_path = root_dir / 'graphics' / "Статистика пользователей.png"
    plt.savefig(plt_path)
    return plt_path

def create_report(requests: list[UserRequest]) -> list[Path]:
    path_to_requests_stats = make_users_stats_graph(requests)
    path_to_users_stats = make_users_stats_graph(requests)
    return [path_to_requests_stats, path_to_users_stats]