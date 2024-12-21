from pathlib import Path

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

from fishing_analysis.request_analyzer import get_stats_from_csv
from fishing_analysis.create_report import (
    make_users_stats_graph,
    make_stats_of_requests_ratio,
    make_stats_of_popular_requests,
    make_stats_of_user_requests,
)
import gradio as gr
from PIL import Image
from gradio.utils import NamedString
from js_scripts import js_func
from css_params import css


def gradio_interface() -> None:
    gr.set_static_paths([root_dir])
    with gr.Blocks(theme=gr.themes.Soft(), js=js_func, css=css) as iface:
        gr.Markdown('# Отчет по собранной статистике с SIEM')

        siem_csv_file = gr.File(label='Загрузить CSV файл')
        load_button = gr.Button('Создать отчет')

        with gr.Row():
            requests_stats_image = gr.Image(
                label='Процентное соотношение фишинговых запросов к легитимным'
            )
            popular_requests_image = gr.Image(label='10 самых популярных запросов')
        users_stats_image = gr.Image(label='Статистика фишинговых запросов по пользователям')

        load_button.click(
            fn=_create_global_report,
            inputs=siem_csv_file,
            outputs=[requests_stats_image, users_stats_image, popular_requests_image],
        )

        gr.Markdown('## Посмотре активности пользователя')
        gr.Markdown('Для просмотра активности пользователя, в поле ввода необходимо указать его адрес IPv4')

        create_user_report = gr.Textbox(label='Введите IPv4')
        user_report_button = gr.Button('Создать отчет по пользователю')
        user_report = gr.DataFrame()
        user_report_button.click(
            fn=_create_user_report, inputs=[siem_csv_file, create_user_report], outputs=user_report
        )

    iface.launch()


def _create_global_report(csv_file: NamedString) -> tuple[Image.Image, Image.Image, Image.Image]:
    requests = get_stats_from_csv(Path(csv_file), root_dir)
    path_to_requests_stats = make_stats_of_requests_ratio(requests, root_dir)
    path_to_users_stats = make_users_stats_graph(requests, root_dir)
    path_to_popular_requests_stats = make_stats_of_popular_requests(requests, root_dir)

    requests_stats_image = Image.open(path_to_requests_stats)
    users_stats_image = Image.open(path_to_users_stats)
    popular_requests_image = Image.open(path_to_popular_requests_stats)

    return requests_stats_image, users_stats_image, popular_requests_image


def _create_user_report(siem_csv_file: NamedString, user_ip: str) -> DataFrame:
    siem_df = pd.read_csv(Path(siem_csv_file))
    user_report = make_stats_of_user_requests(siem_df, user_ip)
    return user_report


if __name__ == '__main__':
    root_dir = Path(__file__).parent.parent.absolute()
    gradio_interface()
