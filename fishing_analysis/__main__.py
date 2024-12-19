from pathlib import Path

from fishing_analysis.request_analyzer import get_stats_from_csv
from fishing_analysis.create_report import make_pie_graph


def fishing_analysis(root_path: Path):
    csv_file = Path("../files/siem_log.csv")
    requests = get_stats_from_csv(csv_file, root_path)
    make_pie_graph(requests)


if __name__ == '__main__':
    root_dir = Path(__file__).parent.parent.absolute()
    fishing_analysis(root_dir)
