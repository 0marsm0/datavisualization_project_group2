import taipy.gui.builder as tgb

with tgb.Page() as page_4:
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()

        with tgb.part():
            tgb.text("This is page 4")
