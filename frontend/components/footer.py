import taipy.gui.builder as tgb


def get_footer():
    with tgb.part(class_name="footer"):
        with tgb.layout(columns="1", align="center", class_name="footer-content"):
            tgb.text("© 2025 Utbildningsanalys | Utvecklad av DE24-Grupp 2", mode="md")
    return tgb.part()
