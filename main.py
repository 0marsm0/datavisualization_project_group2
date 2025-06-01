from taipy.gui import Gui
from frontend.pages.course_page import course_page
from frontend.pages.education_page import page2_page
from frontend.pages.school_page import page_3
from frontend.pages.home import home_page
from frontend.pages.student_page import student_page
from frontend.pages.storytelling import storytelling_page


pages = {
    "hem": home_page,
    "kurser": course_page,
    "utbildning": page2_page,
    "skolor": page_3,
    "studenter": student_page,
    "storytelling": storytelling_page,
}

Gui(pages=pages, css_file="assets/main.css").run(
    dark_mode=False, use_reloader=True, port="auto"
)
