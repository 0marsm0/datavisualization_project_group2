import taipy.gui.builder as tgb
import pandas as pd
from backend.data_processing.course_page_data_processing import (
    course_data_transform,
    available_money,
    table_formatter,
)
from frontend.charts import course_stats, course_school_table, plot_area, plot_map
from frontend.components.header import get_header
from frontend.components.footer import get_footer


def update_state(state):
    state.num_courses = course_stats(df, year=state.year)[0]
    state.approved_courses = course_stats(df, year=state.year)[1]
    state.approved_rate = round(course_stats(df, year=state.year)[2] * 100, 2)
    state.df_course = course_school_table(df, year=state.year)
    state.fig = plot_area(df, year=state.year)
    state.fig2 = plot_map(year=state.year)
    state.tot_rev = round(available_money(state.year)["tot_rev"].sum() / 1e9, 3)
    state.df_course = course_school_table(df, school="", year=state.year)
    state.df_money = table_formatter(state.year).rename(
        columns={"tot_rev": "Beviljat statsbidrag (SEK)"}
    )
    state.df_course_display = pd.merge(
        state.df_course, state.df_money, on="Skola", how="left"
    )[
        [
            "Skola",
            "Antal kurser",
            "Beviljade kurser",
            "Beviljandegrad",
            "Beviljat statsbidrag (SEK)",
        ]
    ]


year = 2024
df = course_data_transform()
df_course = course_school_table(df, school="", year=year)
df_money = table_formatter(year).rename(
    columns={"tot_rev": "Beviljat statsbidrag (SEK)"}
)
df_course_display = pd.merge(df_course, df_money, on="Skola", how="left")[
    [
        "Skola",
        "Antal kurser",
        "Beviljade kurser",
        "Beviljandegrad",
        "Beviljat statsbidrag (SEK)",
    ]
]
num_courses = course_stats(df, year=year)[0]
approved_courses = course_stats(df, year=year)[1]
approved_rate = round(course_stats(df, year=year)[2] * 100, 2)
fig = plot_area(df, year=year)
fig2 = plot_map(year=year)
tot_rev = round(available_money(year)["tot_rev"].sum() / 1e9, 3)


with tgb.Page() as course_page:
    get_header("kurser")

    with tgb.part(class_name="main"):
        with tgb.part(class_name="container"):
            tgb.text("# YH Ansökning för kurser {year}", mode="md")

            with tgb.part(class_name="card description-card"):
                tgb.text(
                    "Denna dashboard visar statistik för kurser inom yrkeshögskolan (YH) i Sverige. "
                    "Här presenteras information om antal sökta och beviljade kurser, beviljandegrad samt tilldelat statsbidrag. "
                    "Interaktiva visualiseringar och tabeller ger en tydlig överblick över beviljade kurser per skola, utbildningsområde och region.",
                    mode="md",
                )

            with tgb.layout("1fr 1fr 1fr 1fr", gap="1rem", class_name="summary-cards"):
                with tgb.part(class_name="card"):
                    tgb.text("###### Sökta kurser", mode="md", class_name="card-h4")
                    tgb.text("### {num_courses}", mode="md")
                with tgb.part(class_name="card"):
                    tgb.text("###### Beviljade kurser", mode="md", class_name="card-h4")
                    tgb.text("### {approved_courses}", mode="md")
                with tgb.part(class_name="card"):
                    tgb.text("###### Beviljandegrad", mode="md", class_name="card-h4")
                    tgb.text("### {approved_rate} %", mode="md")
                with tgb.part(class_name="card"):
                    tgb.text(
                        "###### Tillgängligt statsbidrag",
                        mode="md",
                        class_name="card-h4",
                    )
                    tgb.text("### {tot_rev} md SEK", mode="md")

            with tgb.part(class_name="selector-wrapper"):
                tgb.selector(
                    "{year}",
                    lov=df["År"].unique(),
                    dropdown=True,
                    label="År",
                    on_change=update_state,
                )

            with tgb.part():
                tgb.text("## Topp antal beviljade kurser per skola, {year}", mode="md")
                tgb.text(
                    "*Tabellen är sorterad efter beviljade antal kurser totalt*",
                    mode="md",
                )
                tgb.table("{df_course_display}", page_size=5)

            with tgb.part(class_name="card"):
                tgb.text(
                    "### Beviljade kurser per utbildningsområde, {year}", mode="md"
                )
                tgb.chart(figure="{fig}")

            with tgb.part(class_name="card"):
                tgb.text("### Beviljade kurser per region, {year}", mode="md")
                tgb.chart(figure="{fig2}")

    get_footer()
