import os
import sys

def html_from_file(relative_file_path):
    script_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(script_location, relative_file_path), "r", encoding = "utf8") as html_file:
        return {"raw_html": html_file.read()}
