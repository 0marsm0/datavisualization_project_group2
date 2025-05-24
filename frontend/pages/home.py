import taipy.gui.builder as tgb
from frontend.components.header import get_header


with tgb.Page() as home_page:

    get_header()

    with tgb.part(class_name="main"):
        with tgb.part(class_name="container"):
            tgb.text("# Välkommen till YH dashboard 2024", mode="md")
            with tgb.part(class_name="card"):
                tgb.text(
                    """För att bedriva YH-utbildningar med statligt stöd krävs att varje utbildningsanordnare ansöker om att starta
                    specifika program eller kurser. I ansökningarna måste man visa att utbildningen är förankrad i arbetslivet och att
                    det finns ett faktiskt behov för de kompetenser som utbildningen leder till. Det är här vårt verktyg kommer in. På
                    uppdrag av **The Skool** har vi tagit fram en interaktiv dashboard som ger skolledare, utbildningsledare och annan
                    personal en tydlig överblick över ansökningsomgången 2022 - och mycket mer. Med hjälp av insamlade data visualiserar
                    vi statistik, trender och geografi för att skapa förståelse för YH-utbildningarnas omfattning, resultat och effekt 
                    över tid. Initiativet började med ett proof-of-concept från Kokchun, som med sin dashboard väckt nyfikenhet i 
                    intervjuer med flera yrkeshögskolor. Med Elvins input från utbildningen i Data Engineering, och erfarna ögon för
                    dataanalys, har vi nu vidareutvecklat idén till ett verktyg som stärker beslutsfattandet och förståelsen för
                    YH-utbildningar nationellt.
                    """,
                    mode="md",
                    class_name="text-wrapper taipy-text",
                )
            with tgb.layout("1 1 1 1", class_name="card-wrapper"):
                with tgb.part(class_name="card-link", on_action="goto_kurser"):
                    tgb.text("##### Beviljade kurser", mode="md")
                    with tgb.part(class_name="img-wrapper"):
                        tgb.image(
                            "../../assets/images/01-map.png",
                            class_name="taipy-img img-size",
                        )
                    tgb.text("Antal beviljade kurser per skola geografiskt.")

                with tgb.part(
                    class_name="card-link", on_action="goto_utbildningsomrade"
                ):
                    tgb.text("##### Studerande över tid", mode="md")
                    with tgb.part(class_name="img-wrapper"):
                        tgb.image(
                            "../../assets/images/02-removebg-preview.png",
                            class_name="taipy-img img-size",
                        )
                    tgb.text("Antal studerande över tid per utbildningsområde.")

                with tgb.part(class_name="card-link", on_action="goto_skolor"):
                    tgb.text("##### Statistik per anordnare", mode="md")
                    with tgb.part(class_name="img-wrapper"):
                        tgb.image(
                            "../../assets/images/03-removebg-preview.png",
                            class_name="taipy-img img-size",
                        )
                    tgb.text("Ansökningar, beviljandegrad och utbildningar per skola.")

                with tgb.part(class_name="card-link", on_action="goto_studenter"):
                    tgb.text("##### Studentflöde", mode="md")
                    with tgb.part(class_name="img-wrapper"):
                        tgb.image(
                            "../../assets/images/04.png",
                            class_name="taipy-img img-size",
                        )
                    tgb.text("Från sökande till examinerade – dynamisk funnel-analys.")

    get_footer()
