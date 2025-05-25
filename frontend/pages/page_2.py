"""import taipy.gui.builder as tgb
from frontend.charts import create_educational_area_bar
import pandas as pd
from backend.data_processing.page_2_data_processing import load_and_process_page2_data


def page_2(df_long, raw_data_table):
    # Initiera default state
    number_of_years = 10
    selected_educational_area = df_long["Utbildningsinriktning"].dropna().unique()[0]

    # Första filtrering & initial state
    filtered_data = (
        df_long[df_long["Utbildningsinriktning"] == selected_educational_area]
        .groupby("År")["Antal studerande"]
        .sum()
        .reset_index()
        .sort_values(by="År", ascending=False)
        .head(number_of_years)
    )

    educational_area_chart = create_educational_area_bar(
        df_long, selected_educational_area, number_of_years
    )
    chart_title = f"Antal studerande de senaste {number_of_years} åren inom {selected_educational_area}"
    total_students = int(filtered_data["Antal studerande"].sum())
    average_students = int(filtered_data["Antal studerande"].mean())
    actual_years = filtered_data["År"].nunique()

    # Callback
    def filter_data(state):
        if not state.selected_educational_area or pd.isna(
            state.selected_educational_area
        ):
            return
        filtered = (
            df_long[df_long["Utbildningsinriktning"] == state.selected_educational_area]
            .groupby("År")["Antal studerande"]
            .sum()
            .reset_index()
            .sort_values(by="År", ascending=False)
            .head(state.number_of_years)
        )

        state.educational_area_chart = create_educational_area_bar(
            df_long, state.selected_educational_area, state.number_of_years
        )
        state.chart_title = f"Antal studerande för {state.selected_educational_area}"
        state.total_students = int(filtered["Antal studerande"].sum())
        state.average_students = int(filtered["Antal studerande"].mean())
        state.actual_years = filtered["År"].nunique()

    # Skapa sidan
    with tgb.Page() as page_2:
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part(class_name="container card"):
            tgb.text("# Utbildningsområde {selected_educational_area}", mode="md")
        with tgb.part(class_name="container card stack-large"):
            tgb.text(
                "Denna dashboard visar antal studerande inom olika utbildningsområden på yrkeshögskolan (YH) i Sverige över tid. "
                "Data är hämtad från Statistiska centralbyrån (SCB) och omfattar endast YH-utbildningar. "
                "Genom att filtrera på utbildningsområde och antal år kan du analysera trender och förändringar i antalet studerande "
                "för att få en översikt över utvecklingen inom olika utbildningsinriktningar.",
                mode="md",
            )

            # Statkort
            with tgb.part(class_name="card center"):
                with tgb.layout(columns="1 1", gap="1rem"):
                    with tgb.part():
                        tgb.text(
                            "Totalt antal studerande de senaste {actual_years} åren",
                            mode="md",
                        )
                        tgb.text("## {total_students}", mode="md")

                    with tgb.part():
                        tgb.text("Medelvärdet av studenter per år", mode="md")
                        tgb.text("## {average_students}", mode="md")

                # with tgb.part(class_name="card center"):
                # tgb.text("### Antal år", mode="md")
                # tgb.text("**{actual_years}**", mode="md")

            # Diagram och filter
            with tgb.layout(columns="2 1"):
                with tgb.part(class_name="card"):
                    tgb.text("## {chart_title}", mode="md")
                    tgb.chart(figure="{educational_area_chart}")

                with tgb.part(class_name="card left-margin-md"):
                    tgb.text("## Filtrera data", mode="md")
                    tgb.text("Antal år")
                    tgb.slider(
                        "{number_of_years}", min=1, max=20, step=1, continuous=False
                    )
                    tgb.text("Välj utbildningsområde")
                    tgb.selector(
                        "{selected_educational_area}",
                        lov=df_long["Utbildningsinriktning"].dropna().unique(),
                        dropdown=True,
                    )
                    tgb.button(
                        "FILTRERA DATA",
                        class_name="button-color",
                        on_action=filter_data,
                    )

    return page_2, {
        "number_of_years": number_of_years,
        "selected_educational_area": selected_educational_area,
        "educational_area_chart": educational_area_chart,
        "chart_title": chart_title,
        "raw_data_table": raw_data_table,
        "total_students": total_students,
        "average_students": average_students,
        "actual_years": actual_years,
    }


# Ladda data globalt
df_long, raw_data_table = load_and_process_page2_data()

# Anropa funktionen för att få sidan och initial state
page2_page, page2_state = page_2(df_long, raw_data_table)"""

import taipy.gui.builder as tgb
import pandas as pd
from frontend.charts import create_educational_area_bar
from backend.data_processing.page_2_data_processing import load_and_process_page2_data
from frontend.components.header import get_header
from frontend.components.footer import get_footer


def page_2(df_long, raw_data_table):
    # Initiera default state
    number_of_years = 10
    selected_educational_area = df_long["Utbildningsinriktning"].dropna().unique()[0]

    # Första filtrering & initial state
    filtered_data = (
        df_long[df_long["Utbildningsinriktning"] == selected_educational_area]
        .groupby("År")["Antal studerande"]
        .sum()
        .reset_index()
        .sort_values(by="År", ascending=False)
        .head(number_of_years)
    )

    educational_area_chart = create_educational_area_bar(
        df_long, selected_educational_area, number_of_years
    )
    chart_title = f"Antal studerande de senaste {number_of_years} åren inom {selected_educational_area}"
    total_students = int(filtered_data["Antal studerande"].sum())
    average_students = int(filtered_data["Antal studerande"].mean())
    actual_years = filtered_data["År"].nunique()

    # Callback function for filters
    def on_filter_change(state):
        if not state.selected_educational_area or pd.isna(
            state.selected_educational_area
        ):
            return

        filtered = (
            df_long[df_long["Utbildningsinriktning"] == state.selected_educational_area]
            .groupby("År")["Antal studerande"]
            .sum()
            .reset_index()
            .sort_values(by="År", ascending=False)
            .head(state.number_of_years)
        )

        state.educational_area_chart = create_educational_area_bar(
            df_long, state.selected_educational_area, state.number_of_years
        )
        state.chart_title = f"Antal studerande de senaste {state.number_of_years} åren inom {state.selected_educational_area}"
        state.total_students = int(filtered["Antal studerande"].sum())
        state.average_students = int(filtered["Antal studerande"].mean())
        state.actual_years = filtered["År"].nunique()

    # Page construction with unified styling
    with tgb.Page() as page_2:
        get_header()

        with tgb.part(class_name="main"):
            with tgb.part(class_name="container"):
                # Page title
                tgb.text("# Utbildningsområden", mode="md", class_name="page-title")

                # Description card
                with tgb.part(class_name="card description-card"):
                    tgb.text(
                        "Denna dashboard visar antal studerande inom olika utbildningsområden på yrkeshögskolan (YH) i Sverige över tid. "
                        "Data är hämtad från Statistiska centralbyrån (SCB) och omfattar endast YH-utbildningar. "
                        "Genom att filtrera på utbildningsområde och antal år kan du analysera trender och förändringar.",
                        mode="md",
                    )

                # Combined stats cards and filters row
                with tgb.layout(
                    columns="1 1 1", gap="1.5rem", class_name="combined-controls"
                ):
                    # Stats card 1
                    with tgb.part(class_name="card card-student"):
                        tgb.text("###### Totalt antal", mode="md", class_name="card-h4")
                        tgb.text("#### {total_students}", mode="md")

                    # Stats card 2
                    with tgb.part(class_name="card card-student"):
                        tgb.text("###### Medel per år", mode="md", class_name="card-h4")
                        tgb.text("#### {average_students}", mode="md")

                    # Filters card
                    with tgb.part(class_name="card filters-card"):
                        with tgb.part(class_name="filter-group"):
                            tgb.text("Antal år:", mode="md")
                            tgb.slider(
                                "{number_of_years}",
                                min=1,
                                max=20,
                                step=1,
                                continuous=False,
                                class_name="tgb-slider",
                                on_change=on_filter_change,
                            )

                        with tgb.part(class_name="filter-group"):
                            tgb.text("Utbildningsområde:", mode="md")
                            tgb.selector(
                                "{selected_educational_area}",
                                lov=df_long["Utbildningsinriktning"].dropna().unique(),
                                dropdown=True,
                                class_name="tgb-selector",
                                on_change=on_filter_change,
                            )

                # Main chart area
                with tgb.part(class_name="card chart-wrapper"):
                    tgb.text("## {chart_title}", mode="md")
                    tgb.chart(
                        figure="{educational_area_chart}", class_name="taipy-chart"
                    )

        get_footer()

    return page_2, {
        "number_of_years": number_of_years,
        "selected_educational_area": selected_educational_area,
        "educational_area_chart": educational_area_chart,
        "chart_title": chart_title,
        "raw_data_table": raw_data_table,
        "total_students": total_students,
        "average_students": average_students,
        "actual_years": actual_years,
    }


# Load data
df_long, raw_data_table = load_and_process_page2_data()

# Create page and state
page2_page, page2_state = page_2(df_long, raw_data_table)
