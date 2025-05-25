"""import taipy.gui.builder as tgb
import pandas as pd
import plotly.express as px
from backend.data_processing.page_3_data_processing import load_school_data

# Ladda data
df = load_school_data()
alla_år = sorted(df["År"].unique())
val_år = alla_år[-1]

# Stats- och diagramfunktion
def calculate_state(year):
    filtered = df[df["År"] == year]
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


    # Stapeldiagram: antal utbildningar per skola
    bar_data = filtered["Anordnare"].value_counts().reset_index()
    bar_data = filtered.groupby('Anordnare').size().reset_index(name='Count')
    bar_data.columns = ["Anordnare", "Antal utbildningar"]
    bar_data = bar_data.sort_values(by="Antal utbildningar", ascending=False)
    bar_data = bar_data.head(15)
    fig = px.bar(
        bar_data,
        x="Anordnare",
        y="Antal utbildningar",
        #title=f"Antal utbildningar per anordnare ({year})",
        labels={"Antal utbildningar": "Antal"},
        template="simple_white"
    )

    fig.update_layout(xaxis_tickangle=-45,
                      height=500)

    return antal_ansökningar, antal_beviljade, beviljandegrad, tabell, fig

# Initiera
antal_ansökningar, antal_beviljade, beviljandegrad, skol_tabell, skol_fig = (
    calculate_state(val_år)
)

# Page
with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.navbar()

    with tgb.part(class_name="container card"):
        tgb.text(f"# Statistik per skola, {val_år}", mode="md")

        with tgb.layout(columns="1 1 1"):
            with tgb.part():
                tgb.text("Antal ansökningar")
                tgb.text("### {antal_ansökningar}", mode="md")
            with tgb.part():
                tgb.text("Antal beviljade")
                tgb.text("### {antal_beviljade}", mode="md")
            with tgb.part():
                tgb.text("Beviljandegrad")
                tgb.text("### {beviljandegrad} %", mode="md")

        tgb.text("## Sökta utbildningar per skola, topp 15", mode="md")
        tgb.chart(figure="{skol_fig}")

        tgb.text(f"## Antal utbildningar per skola, {val_år}", mode="md")
        tgb.table(data="{skol_tabell}", page_size=10)"""

import taipy.gui.builder as tgb
import pandas as pd
import plotly.express as px
from backend.data_processing.page_3_data_processing import load_school_data
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
    get_header()

    with tgb.part(class_name="main"):
        with tgb.part(class_name="container"):
            tgb.text("# Statistik per skola {year}", mode="md")

            with tgb.layout("1fr 1fr 1fr", gap="1.5rem", class_name="summary-cards"):
                with tgb.part(class_name="card card-student"):
                    tgb.text("###### Sökta kurser", mode="md", class_name="card-h4")
                    tgb.text("#### {antal_ansökningar}", mode="md")

                with tgb.part(class_name="card card-student"):
                    tgb.text("###### Beviljade kurser", mode="md", class_name="card-h4")
                    tgb.text("#### {antal_beviljade}", mode="md")

                with tgb.part(class_name="card card-student"):
                    tgb.text("###### Beviljandegrad", mode="md", class_name="card-h4")
                    tgb.text("#### {beviljandegrad} %", mode="md")

            with tgb.part(class_name="selector-wrapper"):
                tgb.selector(
                    "{year}",
                    lov=alla_år,
                    dropdown=True,
                    label="År",
                    on_change=on_year_change,
                    class_name="tgb-selector",
                )

            with tgb.part(class_name="card chart-wrapper"):
                tgb.text("## Topp 15 skolor efter antal utbildningar", mode="md")
                tgb.chart(figure="{skol_fig}", class_name="taipy-chart")

            with tgb.part(class_name="card"):
                tgb.text("## Kursstatistik per skola", mode="md")
                tgb.text(
                    "*Tabellen är sorterad efter beviljade antal kurser totalt*",
                    mode="md",
                )
                tgb.table(data="{skol_tabell}", page_size=10, class_name="taipy-table")

    get_footer()
