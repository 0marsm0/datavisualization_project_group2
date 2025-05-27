import taipy.gui.builder as tgb
from backend.data_processing.education_page_data_processing import load_and_process_page2_data
from frontend.charts import create_storytelling_chart, plot_area_storytelling
from backend.data_processing.course_page_data_processing import course_data_transform
from frontend.components.header import get_header


# Ladda och processa data
df_long, _ = load_and_process_page2_data()

# Grupp och summering enligt tidigare
df_summary = df_long.groupby("Utbildningsinriktning", as_index=False)[
    "Antal studerande"
].sum()

fig = create_storytelling_chart(df_summary)
bar_chart = plot_area_storytelling(course_data_transform(), 2024)


with tgb.Page() as storytelling_page:
    get_header("storytelling")
    with tgb.part(class_name="main"):
        # tgb.navbar()
        with tgb.part(class_name="container"):
            tgb.text("# Stockholms Tekniska Institut", mode="md")
            tgb.text("### Fokusområden och dess framtid", mode="md")

        with tgb.part(class_name="card"):
            tgb.image(
                "assets/figures/storytelling_education.png",
                width=1600,
                height=1000,
                scale=2,
            )

        with tgb.part(class_name="card"):
            tgb.image(
                "assets/figures/storytelling_course.png",
                width=1400,
                height=1000,
                scale=2,
            )
