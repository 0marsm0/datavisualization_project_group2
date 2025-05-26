import taipy.gui.builder as tgb
from frontend.components.header import get_header
from frontend.components.footer import get_footer


def get_layout(current_page, content_part):
    with tgb.Page() as layout:
        get_header(current_page)
        tgb.part(content=content_part)
        get_footer()
    return layout
