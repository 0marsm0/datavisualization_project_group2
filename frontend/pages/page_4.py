import taipy.gui.builder as tgb
from taipy.gui import Gui
import plotly.express as px
import pandas as pd
from frontend.charts import create_funnel_chart_total, create_funnel_chart_gender
from backend.data_processing.page_4_data_processing import (
    get_direction_and_year_options,
    prepare_total_data,
    prepare_gender_comparison_funnel_data,
)
from frontend.components.header import get_header
from frontend.components.footer import get_footer

directions, years = get_direction_and_year_options()
default_direction = "Totalt" if "Totalt" in directions else directions[0]
default_year = max(years)
default_view = "Totalt"


direction = default_direction
year = default_year
funnel_view = default_view


initial_df = prepare_total_data(direction, year)
funnel_fig = create_funnel_chart_total(initial_df)


def update_state(state):
    if state.funnel_view == "Totalt":
        df = prepare_total_data(state.direction, state.year)
        state.funnel_fig = create_funnel_chart_total(df)
    elif state.funnel_view == "Kön":
        df = prepare_gender_comparison_funnel_data(state.direction, state.year)
        state.funnel_fig = create_funnel_chart_gender(df)


with tgb.Page() as student_page:

    get_header()

    with tgb.part(class_name="main"):
        with tgb.part(class_name="container"):
            tgb.text("# Utbildningsanalys — Funnel chart", mode="md")
            with tgb.part():
                tgb.text(
                    "##### Dynamisk analys av studentflöde: *sökande → behöriga → antagna → examinerade*.",
                    mode="md",
                )
            with tgb.layout("1fr 1fr 1fr 1fr", gap="1rem", class_name="summary-cards"):
                with tgb.part(class_name="card"):
                    tgb.text("##### Sökande", mode="md")
                    tgb.text("#### 12000", mode="md")
                with tgb.part(class_name="card"):
                    tgb.text("##### Behöriga", mode="md")
                    tgb.text("#### 9000", mode="md")
                with tgb.part(class_name="card"):
                    tgb.text("##### Antagna", mode="md")
                    tgb.text("#### 6000", mode="md")
                with tgb.part(class_name="card"):
                    tgb.text("##### Examinerade", mode="md")
                    tgb.text("#### 3000", mode="md")
            with tgb.part():
                with tgb.layout("1fr 1fr 1fr", gap="1rem", class_name="filters"):
                    with tgb.part():
                        tgb.selector(
                            "{year}",
                            lov=years,
                            dropdown=True,
                            label="År",
                            on_change=update_state,
                            class_name="tgb-selector",
                        )
                    with tgb.part():
                        tgb.selector(
                            "{direction}",
                            lov=directions,
                            dropdown=True,
                            label="Utbildningsområde",
                            on_change=update_state,
                            class_name="tgb-selector",
                            id="study-selector",
                        )
                    with tgb.part():
                        tgb.selector(
                            "{funnel_view}",
                            lov=["Totalt", "Kön"],
                            dropdown=True,
                            label="Visa som",
                            radio=True,
                            multiple=False,
                            on_change=update_state,
                            class_name="tgb-selector",
                        )

            with tgb.part(class_name="card chart-wrapper"):
                tgb.chart(figure="{funnel_fig}", class_name="taipy-chart")

    get_footer()
