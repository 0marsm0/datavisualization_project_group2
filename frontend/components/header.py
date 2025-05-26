import taipy.gui.builder as tgb


def get_header(current_page):
    def is_active(page):
        return "nav-button active" if page == current_page else "nav-button"

    with tgb.part(class_name="header sticky"):
        with tgb.layout(
            columns="auto auto 1 auto",
            align="center",
            gap="1rem",
            class_name="navbar-content",
        ):
            tgb.text("📊 The Skool Dashboard", id="logo")
            tgb.navbar()
            # with tgb.layout(columns="auto auto auto auto auto auto", gap="auto"):
            #     tgb.button("Hemsida", class_name=is_active("hem"), url="/hem")
            #     tgb.button("Kurser", class_name=is_active("kurser"), url="/kurser")
            #     tgb.button(
            #         "Utbildning", class_name=is_active("utbildning"), url="/utbildning"
            #     )
            #     tgb.button("Skolor", class_name=is_active("skolor"), url="/skolor")
            #     tgb.button(
            #         "Studenter", class_name=is_active("studenter"), url="/studenter"
            #     )
            #     tgb.button(
            #         "Storytelling",
            #         class_name=is_active("storytelling"),
            #         url="/storytelling",
            #     )
    return tgb.part()
