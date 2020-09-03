from html.parser import HTMLParser as BaseHTMLParser


class HTMLParser(BaseHTMLParser):
    data = []
    columns = []
    recording = False

    def feed(self, *args, **kwargs):
        self.data = []
        super().feed(*args, **kwargs)

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.columns = []
            self.recording = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.recording = False
            if self.columns:
                self.data.append(self.columns)

    def handle_data(self, data):
        if self.recording and not self.lasttag == 'th':
            self.columns.append(data)
