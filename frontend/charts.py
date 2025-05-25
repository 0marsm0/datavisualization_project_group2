import duckdb
import plotly.express as px
import plotly.graph_objects as go
from backend.data_processing.page_1_data_processing import map_df, geo_file


# CHARTS AND STATS FOR THE COURSE PAGE (PAGE 1)
# stats on top of course page
def course_stats(df, **options):
    if "year" in options:
        selected_year = options.get("year")
        total_count = duckdb.query(
            f"""--sql
                 SELECT COUNT(*) as count
                 FROM df
                WHERE "År" = {selected_year}
        """
        ).df()
        total_count = total_count.iloc[0, 0]
        total_approved = duckdb.query(
            f"""--sql
                SELECT COUNT(*) as count
                FROM df
                WHERE "År" = {selected_year} AND "Beslut" = 'Beviljad'
        """
        ).df()
        total_approved = total_approved.iloc[0, 0]
        approved_rate = total_approved / total_count
    return (total_count, total_approved, approved_rate)


# table for the course page
def course_school_table(df, school="", year=2024):
    if school == "":
        df = duckdb.query(
            f"""--sql
                SELECT 
                skola,
                COUNT(kursnamn) AS "Antal kurser",
                COUNT(CASE WHEN "Beslut"= 'Beviljad' THEN 1 ELSE NULL END) AS "Beviljade kurser",
                "Beviljade kurser"/ "Antal kurser" AS rate
                FROM df
                WHERE "År" = {year}
                GROUP BY skola
                ORDER BY "Antal kurser" DESC
        """
        ).df()
        df["rate"] = round((df["rate"] * 100), 2).astype(str) + "%"
        df = df.rename(columns={"rate": "Beviljandegrad"})
        return df
    else:
        df = duckdb.query(
            f"""--sql
                SELECT 
                skola,
                COUNT(kursnamn) AS antal_kurser,
                COUNT(CASE WHEN "Beslut"= 'Beviljad' THEN 1 ELSE NULL END) AS approved_courses,
                approved_courses/ antal_kurser AS rate
                FROM df
                WHERE "År" = {year} AND skola = '{school}'
                GROUP BY skola  
                ORDER BY antal_kurser DESC
        """
        ).df()
        return df


# plot the bar chart for area of education
def plot_area(df, year):
    duckdb.register("df_for_query", df)
    plot_df = duckdb.query(
        f"""--sql
            SELECT Utbildningsområde, COUNT(*) as antal, Beslut
            FROM df
            WHERE År = {year}
            GROUP BY Utbildningsområde, Beslut
                        ORDER BY antal DESC
        """
    ).df()

    custom_colors = {
        "Beviljad": "#084083",  # Color for Approved
        "Avslag": "#ff5e4d",  # Color for Rejected
    }

    fig = px.bar(
        plot_df,
        x="antal",
        y="Utbildningsområde",
        color="Beslut",
        color_discrete_map=custom_colors,
        orientation="h",
        text_auto=True,
        height=800,
    )
    fig.update_layout(
        showlegend=False,
        barmode="group",
        plot_bgcolor="white",
        yaxis=dict(autorange="reversed"),
        xaxis=dict(title="Antal"),
        font=dict(color="white"),
    )
    return fig


# plot the map on course page
def plot_map(year):

    color_scale = [
        "#fdd8d3",
        "#fa4531",
    ]
    df_map = map_df(year)
    df_map = df_map.rename(columns={"antal_bev": "Antal beviljade", "code": "Länskod"})
    geo_json = geo_file()
    fig = px.choropleth(
        df_map,
        geojson=geo_json,
        locations="Länskod",
        featureidkey="properties.ref:se:länskod",
        color="Antal beviljade",
        color_continuous_scale=color_scale,
        hover_name="name",
    )

    fig.update_layout(width=1000, height=700, legend=dict(title="Antal beviljade"))
    fig.update_geos(
        fitbounds="locations", visible=False, projection_type="orthographic"
    )

    return fig


def create_funnel_chart_total(df):
    fig = px.funnel(
        df,
        x="value",
        y="stage",
        title="Utbildningsfunnel: Total antal studenter",
    )
    fig.update_layout(
        plot_bgcolor="#1f2f44",
        xaxis_title="Antal personer",
        yaxis_title="Steg",
        font=dict(color="white"),
    )
    fig.update_xaxes(title_text=None)
    fig.update_yaxes(title_text=None)
    return fig


def create_funnel_chart_gender(df):
    fig = px.funnel(
        df,
        x="number",
        y="stage",
        color="office",
        title="Utbildningsfunnel (Kön)",
    )
    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Antal personer",
        yaxis_title="Steg",
        font=dict(color="white"),
        legend=dict(
            bgcolor="#1f2f44",
        ),
        legend_title_text="",
    )
    fig.update_xaxes(title_text=None)
    fig.update_yaxes(title_text=None)
    return fig


# CHARTS AND STATS FOR STORYTELLING PAGE (storytelling 2)


def create_storytelling_chart(df_summary):
    highlight_area = "Ekonomi, administration och försäljning"
    colors = [
        "lightgray" if area != highlight_area else "royalblue"
        for area in df_summary["Utbildningsinriktning"]
    ]

    fig_px = px.bar(
        df_summary,
        y="Utbildningsinriktning",
        x="Antal studerande",
        orientation="h",
        title="Vilket utbildningsområde bör # The Skool fokusera på ?",
        labels={
            "Utbildningsinriktning": "Utbildningsområde",
            "Antal studerande": "Antal studerande",
        },
    )

    fig_px.update_traces(marker_color=colors)
    fig_px.update_layout(
        plot_bgcolor="white",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        margin=dict(l=120, r=80, t=80, b=40),
    )

    if highlight_area in df_summary["Utbildningsinriktning"].values:
        highlight_idx = df_summary.index[
            df_summary["Utbildningsinriktning"] == highlight_area
        ][0]
        highlight_value = df_summary.loc[highlight_idx, "Antal studerande"]

        fig_px.add_annotation(
            x=highlight_value,
            y=highlight_idx - 0.4,
            text=" Viktig tillväxtmöjlighet",
            showarrow=True,
            arrowhead=3,
            arrowcolor="royalblue",
            ax=0,
            ay=30,
            font=dict(color="royalblue", size=13, family="Arial"),
            bgcolor="white",
            bordercolor="royalblue",
            borderwidth=1,
        )

    # Konvertera plotly.express-figuren till plotly.graph_objects.Figure
    fig = go.Figure(fig_px)
    return fig


# Storytelling graf för kurser
def plot_area_storytelling(df, year=2024):
    duckdb.register("df_for_query", df)
    plot_df = duckdb.query(
        f"""--sql
            SELECT Utbildningsområde, COUNT(*) as antal, Beslut
            FROM df
            WHERE År = {year}
            GROUP BY Utbildningsområde, Beslut
                        ORDER BY antal DESC
        """
    ).df()

    bar_colors = {
        "Beviljad": "#084083",
        "Avslag": "#E4ECF6",
    }

    unique_utbildningsomrade = plot_df["Utbildningsområde"].unique().tolist()
    tick_vals = list(range(len(unique_utbildningsomrade)))
    tick_texts = []
    for category in unique_utbildningsomrade:
        if category == "Data/IT":
            tick_texts.append(
                f"<span style='color:black; font-weight: bold; font-size: 1.1em;'>{category}</span>"
            )
        elif category == "Samhällsbyggnad och byggteknik":
            tick_texts.append(
                f"<span style='color:black; font-weight: bold; font-size: 1.1em;'>{category}</span>"
            )
        else:
            tick_texts.append(f"<span style='color:#a9a9a9'>{category}</span>")

    fig = px.bar(
        plot_df,
        x="antal",
        y="Utbildningsområde",
        color="Beslut",
        color_discrete_map=bar_colors,
        orientation="h",
        text_auto=True,
        height=800,
        title=r"Stor skillnad i beviljandegrad för STIs huvudområden. Data/IT<br>har både mer sökta kurser och majoriteten avslagna",
    )
    fig.update_layout(
        showlegend=False,
        barmode="group",
        plot_bgcolor="white",
        yaxis=dict(
            autorange="reversed",
            title="",
            tickmode="array",
            tickvals=tick_vals,
            ticktext=tick_texts,
        ),
        xaxis=dict(title=r"<b>ANTAL</b>"),
        title=dict(font=dict(size=24), x=0.1, y=0.925),
        margin=dict(l=0, t=150),
    )

    fig.add_annotation(
        text=r"<b>UTBILDNINGSOMRÅDE</b>",
        yref="paper",
        xref="paper",
        x=-0.27,
        y=1.04,
        showarrow=False,
        align="right",
        font=dict(size=14),
    )

    fig.add_annotation(
        text=r"Utbildningsområde med<br><b>hög</b> beviljandegrad",
        yref="paper",
        xref="paper",
        x=0.595,
        y=0.72,  # position
        showarrow=True,
        # --- Arrowhead ---
        ax=30,  # X-koordinater var pilen pekar
        ay=60,  # Y-koord
        axref="pixel",  #'ax' som värde på x-axeln
        ayref="pixel",
        arrowhead=5,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="black",
        standoff=1,
        startstandoff=1,
        align="left",
        font=dict(size=10),
    )
    fig.add_annotation(
        text=r"Utbildningsområde med<br><b>låg</b> beviljandegrad",
        yref="paper",
        xref="paper",
        x=0.7,
        y=0.89,
        ax=30,
        showarrow=True,
        ay=60,
        axref="pixel",
        arrowhead=5,
        ayref="pixel",
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="black",
        standoff=1,
        startstandoff=1,
        align="left",
        font=dict(size=10),
    )
    fig.add_annotation(
        text=r"Data från ansökningsomgång myh kurser 2024",
        yref="paper",
        xref="paper",
        x=0.88,
        y=0.05,
        showarrow=False,
        align="left",
        font=dict(size=12, color="#a9a9a9"),
    )

    fig.add_layout_image(
        dict(
            source="download.jpeg",
            xref="paper",
            yref="paper",
            x=0.98,
            y=0.03,
            sizex=0.15,
            sizey=0.15,
        )
    )
    return fig


# Page 2
def create_educational_area_bar(df, selected_area, num_years=5):
    # Filtrera de senaste num_years åren
    recent_years = sorted(df["År"].unique())[-num_years:]
    filtered = df[df["År"].isin(recent_years)]

    # Summera per inriktning och år
    grouped = (
        filtered.groupby(["År", "Utbildningsinriktning"])["Antal studerande"]
        .sum()
        .reset_index()
    )

    # Skapa grundgraf med alla utbildningsområden
    fig = go.Figure()

    for area in grouped["Utbildningsinriktning"].unique():
        area_data = grouped[grouped["Utbildningsinriktning"] == area]
        fig.add_trace(
            go.Scatter(
                x=area_data["År"],
                y=area_data["Antal studerande"],
                mode="lines+markers",
                name=area,
                line=dict(
                    width=4 if area == selected_area else 1.5,
                    color="#0077b6" if area == selected_area else "#cccccc",
                ),
                marker=dict(size=6 if area == selected_area else 4),
                opacity=1.0 if area == selected_area else 0.4,
                hovertemplate=f"{area}<br>År: %{{x}}<br>Antal studerande: %{{y}}<extra></extra>",
            )
        )

    fig.update_layout(
        title=None,
        xaxis=dict(
            title="År", tickangle=0, title_font=dict(size=14), tickfont=dict(size=12)
        ),
        yaxis=dict(
            title="Antal studerande", title_font=dict(size=14), tickfont=dict(size=12)
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Arial", size=14),
        margin=dict(t=20, b=40, l=60, r=20),
        hovermode="x unified",
        showlegend=False,
    )

    return fig
