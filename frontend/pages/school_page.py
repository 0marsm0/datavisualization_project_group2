import taipy.gui.builder as tgb
import pandas as pd
import plotly.express as px
from backend.data_processing.school_page_data_processing import load_school_data
from frontend.components.header import get_header
from frontend.components.footer import get_footer

# Ladda data
df = load_school_data()
alla_år = sorted(df["År"].unique(), reverse=True)
val_år = alla_år[0]


class State:
    def __init__(self, year):
        self.year = year


# Stats- och diagramfunktion
def calculate_state(state):
    filtered = df[df["År"] == state.year]
    antal_ansökningar = len(filtered)
    antal_beviljade = len(filtered[filtered["Status"] == "Beviljad"])
    beviljandegrad = (
        round(antal_beviljade / antal_ansökningar * 100, 2)
        if antal_ansökningar > 0
        else 0
    )

    # Tabell per skola
    tabell = (
        filtered.groupby(["Anordnare", "Status"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    tabell = tabell.sort_values(by=["Beviljad", "Avslag"], ascending=[False, False])
    tabell_display = tabell.rename(
        columns={
            "Anordnare": "Skola",
            "Beviljad": "Beviljade kurser",
            "Avslag": "Avslagna kurser",
        }
    )

    # Stapeldiagram: antal utbildningar per skola
    bar_data = filtered["Anordnare"].value_counts().reset_index()
    bar_data = filtered.groupby("Anordnare").size().reset_index(name="Count")
    bar_data.columns = ["Anordnare", "Antal utbildningar"]
    bar_data = bar_data.sort_values(by="Antal utbildningar", ascending=False).head(15)

    fig = px.bar(
        bar_data,
        x="Anordnare",
        y="Antal utbildningar",
        labels={"Antal utbildningar": "Antal"},
        template="plotly_dark",
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
    )

    return antal_ansökningar, antal_beviljade, beviljandegrad, tabell_display, fig


# Initiera state
initial_state = State(val_år)
antal_ansökningar, antal_beviljade, beviljandegrad, skol_tabell, skol_fig = (
    calculate_state(initial_state)
)


# Callback function
def on_year_change(state):
    (
        state.antal_ansökningar,
        state.antal_beviljade,
        state.beviljandegrad,
        state.skol_tabell,
        state.skol_fig,
    ) = calculate_state(state)


# Page
with tgb.Page() as page_3:
    get_header("skolor")

    with tgb.part(class_name="main"):
        with tgb.part(class_name="container"):
            tgb.text("# Statistik per skola, 2024", mode="md")

            with tgb.layout("1fr 1fr 1fr", gap="1.5rem", class_name="summary-cards"):
                with tgb.part(class_name="card card-student"):
                    tgb.text(
                        "###### Sökta utbildningar", mode="md", class_name="card-h4"
                    )
                    tgb.text("#### {antal_ansökningar}", mode="md")

                with tgb.part(class_name="card card-student"):
                    tgb.text(
                        "###### Beviljade utbildningar", mode="md", class_name="card-h4"
                    )
                    tgb.text("#### {antal_beviljade}", mode="md")

                with tgb.part(class_name="card card-student"):
                    tgb.text("###### Beviljandegrad", mode="md", class_name="card-h4")
                    tgb.text("#### {beviljandegrad} %", mode="md")

            # with tgb.part(class_name="selector-wrapper"):
            #     tgb.selector(
            #         "{year}",
            #         lov=alla_år,
            #         dropdown=True,
            #         label="År",
            #         on_change=on_year_change,
            #         class_name="tgb-selector",
            #     )

            with tgb.part(class_name="card chart-wrapper"):
                tgb.text(
                    "## Topp 15 skolor efter antal sökta utbildningar, 2024", mode="md"
                )
                tgb.chart(figure="{skol_fig}", class_name="taipy-chart")

            with tgb.part(class_name="card"):
                tgb.text("## Sökta utbildningar per skola", mode="md")
                tgb.text(
                    "*Tabellen är sorterad efter beviljade antal utbildningar totalt*",
                    mode="md",
                )
                tgb.table(data="{skol_tabell}", page_size=10, class_name="taipy-table")

    get_footer()
