from pathlib import Path

from fishing_analysis.request_analyzer import get_stats_from_csv
from fishing_analysis.create_report import make_users_stats_graph, make_pie_graph
import gradio as gr
from PIL import Image


def gradio_interface() -> None:
    gr.set_static_paths([root_dir])
    with gr.Blocks() as iface:
        gr.Markdown('Отчет по собранной статистике с SIEM')

        csv_file = gr.File(label='Загрузить CSV файл')
        load_button = gr.Button('Создать отчет')

        with gr.Row():
            image1 = gr.Image(label='Процентное соотношение фишинговых запросов к легитимным')
            image2 = gr.Image(label='Статистика фишинговых запросов по пользователям')

        load_button.click(fn=_create_report, inputs=csv_file, outputs=[image1, image2])

    iface.launch()


def _create_report(csv_file: Path) -> tuple[Image.Image, Image.Image]:
    requests = get_stats_from_csv(Path(csv_file), root_dir)
    path_to_requests_stats = make_pie_graph(requests, root_dir)
    path_to_users_stats = make_users_stats_graph(requests, root_dir)

    requests_stats_image = Image.open(path_to_requests_stats)
    users_stats_image = Image.open(path_to_users_stats)

    return requests_stats_image, users_stats_image


if __name__ == '__main__':
    root_dir = Path(__file__).parent.parent.absolute()
    gradio_interface()
