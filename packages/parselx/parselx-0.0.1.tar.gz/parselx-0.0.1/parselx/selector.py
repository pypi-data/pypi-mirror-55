from parsel import Selector, SelectorList

from .process import process as _process


class SelectorListX(SelectorList):
    def x(self, query):
        return _process(self, query)


class SelectorX(Selector):
    selectorlist_cls = SelectorListX

    def x(self, query):
        return _process(self, query)
