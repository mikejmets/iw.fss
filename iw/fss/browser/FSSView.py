from Products.Five import BrowserView


class FSSView(BrowserView):
    def mytry(self):
        return "OK"