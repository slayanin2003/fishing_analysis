from fishing_analysis.types_module import UserRequest, UserFishingStats
import matplotlib.pyplot as plt


def _create_users_stats(requests: list[UserRequest]) -> list[UserFishingStats]:
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
    plt.show()


def make_users_stats_graph(requests: list[UserRequest]) -> None:
    user_request_stats = _create_users_stats(requests)
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
    plt.show()