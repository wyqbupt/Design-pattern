#!/usr/bin/env python3
import sys
import textwrap
import abc
import collections


# Thanks to Nick Coghlan for these!
if sys.version_info[:2] >= (3, 3):
    class Renderer(metaclass=abc.ABCMeta):

        @classmethod
        def __subclasshook__(Class, Subclass):
            if Class is Renderer:
                attributes = collections.ChainMap(*(Superclass.__dict__
                        for Superclass in Subclass.__mro__))
                methods = ("header", "paragraph", "footer")
                if all(method in attributes for method in methods):
                    return True
            return NotImplemented
else:
    class Renderer(metaclass=abc.ABCMeta):

        @classmethod
        def __subclasshook__(Class, Subclass):
            if Class is Renderer:
                needed = {"header", "paragraph", "footer"}
                for Superclass in Subclass.__mro__:
                    for meth in needed.copy():
                        if meth in Superclass.__dict__:
                            needed.discard(meth)
                    if not needed:
                        return True
            return NotImplemented


class Page:
    def __init__(self, title, renderer):
        if not isinstance(renderer, Renderer):
            raise TypeError("Expected object of type Renderer, got {}".format(type(renderer).__name__))
        self.title = title
        self.renderer = renderer
        self.paragraphs = []

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph)

    def render(self):
        self.renderer.header(self.title)
        for paragraph in self.paragraphs:
            self.renderer.paragraph(paragraph)
        self.renderer.footer()


class TextRenderer:

    def __init__(self, width=80, file=sys.stdout):
        self.width = width
        self.file = file
        self.previous = False

    def header(self, title):
        self.file.write("{0:^{2}}\n{1:^{2}}\n".format(title, "=" * len(title), self.width))

    def paragraph(self, text):
        if self.previous:
            self.file.write("\n")
        self.file.write(textwrap.fill(text, self.width))
        self.file.write("\n")
        self.previous = True

    def footer(self):
        pass


MESSAGE = """This is a very short {} paragraph that demonstrates
the simple {} class."""


def main():
    paragraph1 = MESSAGE.format("plain-text", "TextRenderer")
    paragraph2 = """This is another short paragraph just so that we can
        see two paragraphs in action."""
    title = "Plain Text"
    textPage = Page(title, TextRenderer(22))
    textPage.add_paragraph(paragraph1)
    textPage.add_paragraph(paragraph2)
    textPage.render()
    print()


if __name__ == "__main__":
    main()
