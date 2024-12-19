import csv

from neural_network.network import predict
from fishing_analysis.types_module import UserRequest
from pathlib import Path


def load_requests_from_csv(file_path: Path) -> list[UserRequest]:
    requests = []
    try:
        with open(file_path.as_posix(), mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                requests.append(UserRequest(ip=row['DestinationIP'], url=row['DnsQuery']))
    except Exception as e:
        raise ValueError(f"Ошибка при загрузке файла: {e}")
    return requests


def analyze_requests(requests: list[UserRequest], root_path: Path) -> None:
    for request in requests:
        prediction = predict(request.url, root_path)
        request.valid = 0 if prediction == "Легитимный" else 1 # 0 - Легитимный, 1 - Фишинговый


def get_stats_from_csv(csv_path: Path, root_path: Path) -> list[UserRequest]:
    requests = load_requests_from_csv(csv_path)
    analyze_requests(requests, root_path)
    return requests


if __name__ == '__main__':
    root_dir = Path(__file__).parent.parent.absolute()
    csv_file = Path("../files/siem_log.csv")
    get_stats_from_csv(csv_file, root_dir)
