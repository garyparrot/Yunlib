from linebot.models import *
from .styles import *

class config:

    def __init__(self, books = list(), lfooter = "footer", rfooter = "footer", title = "Title", emptyhint = "Nothing"):
        self.lfooter = lfooter
        self.rfooter = rfooter
        self.books   = books
        self.title   = title
        self.emptyhint = emptyhint

class style:
    
    def __init__(self):
        self.lfooter            = compose( text0, cgrey1, flex0 )
        self.rfooter            = compose( text0, cgrey1, align_end )
        self.footer             = compose( horizontal, margin2 )
        self.title              = compose( bold, cgreen, text2 )
        self.section_title      = compose( bold, margin1, text5, flex7 )
        self.section_subtitle   = compose( wrap, cgrey1, text0, align_end, gbottom, flex3 )
        self.emptyhint          = compose( cgrey2, margin5, text1, align_center )
        self.bookname_style     = compose( flex7, text1, cgrey2 )
        self.bookduedate_style  = compose( flex3, text1, cblack, align_end )

class MyBooklistRender:

    def __init__(self, config = config(), style = style()):
        self.config = config
        self.style = style

    def render(self):
        return BubbleContainer(
                body   = self.renderBody(),
                footer = self.renderFooter(),
                styles = self.renderBubbleStyle()
                )

    """ Body of booklist """
    def renderBody(self):

        result = [self.renderTitle()]
        sections = {  }

        # Rearrange books
        for book in self.config.books:
            if book.library_name in sections:
                sections[book.library_name].append(book)
            else:
                sections[book.library_name] = [ book ]

        # Add content
        if len(self.config.books) == 0:
            result.append(self.renderEmptyHint())
        else:
            for name, section in sections.items():
                result.append(self.renderSection(name, f"{len(section)} books", section))

        return BoxComponent(contents = result, layout = "vertical")

    """ If there is no book, put this instead """
    def renderEmptyHint(self):
        return TextComponent(text = self.config.emptyhint, **self.style.emptyhint)

    """ section of booklist """
    def renderSection(self, section_title, section_subtitle, books):
        section_title    = TextComponent(text=section_title, **self.style.section_title)
        section_subtitle = TextComponent(text=section_subtitle, **self.style.section_subtitle)
        title_area = BoxComponent(contents = [ section_title, section_subtitle ], layout = "horizontal")
        sep = SeparatorComponent( **margin2 )

        return BoxComponent( contents = [ title_area, sep, *[ self.renderBook(book) for book in books ] ], layout = "vertical")

    """ render book itself """
    def renderBook(self, book):
        bookname = TextComponent(text = book.bookname, **self.style.bookname_style)
        duedate  = TextComponent(text = book.duedate , **self.style.bookduedate_style)

        return BoxComponent( contents = [bookname, duedate], layout = "horizontal")

    """ Title of Booklist """
    def renderTitle(self):
        return TextComponent(text=self.config.title, **self.style.title)

    """ Footer of Booklist """
    def renderFooter(self):
        lfoot = TextComponent(text=self.config.lfooter, **self.style.lfooter)
        rfoot = TextComponent(text=self.config.rfooter, **self.style.rfooter)
        return BoxComponent( contents = [lfoot, rfoot], **self.style.footer )

    def renderBubbleStyle(self):
        return BubbleStyle( footer = BlockStyle( separator = True ))
