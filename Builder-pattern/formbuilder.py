#!/usr/bin/env python3
import abc
import os
import tempfile
import sys
if sys.version_info[:2] < (3, 2):
    from xml.sax.saxutils import escape
else:
    from html import escape
class AbstractFormBuilder(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def add_title(self, title):
        self.title = title

    @abc.abstractmethod
    def form(self):
        pass

    @abc.abstractmethod
    def add_label(self, text, row, column, **kwargs):
        pass

    @abc.abstractmethod
    def add_entry(self, variable, row, column, **kwargs):
        pass

    @abc.abstractmethod
    def add_button(self, text, row, column, **kwargs):
        pass

class HtmlFormBuilder(AbstractFormBuilder):
    def __init__(self):
        self.title = "HtmlFormBuilder"
        self.items = {}

    def add_title(self, title):
        super().add_title(escape(title))

    def add_label(self, text, row, column, **kwargs):
        self.items[(row, column)] = ('<td><label for="{}">{}:</label></td>'.format(kwargs["target"], escape(text)))

    def add_entry(self, variable, row, column, **kwargs):
        html = """<td><input name="{}" type="{}" /></td>""".format(variable, kwargs.get("kind", "text"))
        self.items[(row, column)] = html

    def add_button(self, text, row, column, **kwargs):
        html = """<td><input type="submit" value="{}" /></td>""".format(escape(text))
        self.items[(row, column)] = html

    def form(self):
        html = ["<!doctype html>\n<html><head><title>{}</title></head>"
            "<body>".format(self.title), '<form><table border="0">']
        thisRow = None
        for key,value in sorted(self.items.items()):
            row, column = key
            if thisRow is None:
                html.append(" <tr>")
            elif thisRow != row:
                html.append("  </tr>\n  <tr>")
            thisRow = row
            html.append("    " + value)
        html.append("  </tr>\n</table></form></body></html>")
        return "\n".join(html)
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-P": # For regression testing
        print(create_login_form(HtmlFormBuilder()))
        print(create_login_form(TkFormBuilder()))
        return
    htmlFilename = os.path.join(tempfile.gettempdir(), "login.html")
    htmlForm = create_login_form(HtmlFormBuilder())
    with open(htmlFilename, "w", encoding="utf-8") as file:
        file.write(htmlForm)
        print("wrote", htmlFilename)

def create_login_form(builder):
    builder.add_title("Login")
    builder.add_label("Username", 0, 0, target="username")
    builder.add_entry("username", 0, 1)
    builder.add_label("Password", 1, 0, target="password")
    builder.add_entry("password", 1, 1, kind="password")
    builder.add_button("Login", 2, 0)
    builder.add_button("Cancel", 2, 1)
    return builder.form()

if __name__ == "__main__":
    main()
    
