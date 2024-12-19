from fishing_analysis.types_module import UserRequest
import matplotlib.pyplot as plt


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