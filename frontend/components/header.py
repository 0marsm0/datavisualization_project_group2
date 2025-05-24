import taipy.gui.builder as tgb


def get_header():
    with tgb.part(class_name="header sticky"):
        with tgb.layout(
            columns="auto auto 1 auto",
            align="center",
            gap="1rem",
            class_name="navbar-content container",
        ):
            tgb.text("Dashboard Name", id="logo")

            with tgb.layout(columns="auto auto auto auto auto auto", gap="auto"):
                tgb.button("Hemsida", class_name="nav-button active")
                tgb.button("Kurser", class_name="nav-button")
                tgb.button("Utbildning", class_name="nav-button")
                tgb.button("Skolor", class_name="nav-button")
                tgb.button("Studenter", class_name="nav-button")
                tgb.button("Storytelling", class_name="nav-button")
    return tgb.part()
