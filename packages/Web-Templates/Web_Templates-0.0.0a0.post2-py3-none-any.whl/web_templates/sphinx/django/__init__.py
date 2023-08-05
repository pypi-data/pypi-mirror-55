from os import path

def setup(app) :
 app.add_html_theme("sphinx_django", path.abspath(path.dirname(__file__)))