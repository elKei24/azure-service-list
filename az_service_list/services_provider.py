import re
from collections import defaultdict
from enum import Enum
from html.parser import HTMLParser
from typing import Dict, Set

import requests

URL = "https://azure.microsoft.com/en-us/products"


def get_services() -> Dict[str, Set[str]]:
    parser = _ProductsHtmlParser()
    html = _get_products_html()
    parser.feed(html)
    return parser.products


def _get_products_html() -> str:
    return requests.get(URL).text


class _TagType(Enum):
    OTHER = 1
    PRODUCT = 2
    CATEGORY = 3


class _ProductsHtmlParser(HTMLParser):
    _next_data_type: _TagType = _TagType.OTHER
    _current_category: str | None = None
    products: Dict[str, Set[str]] = defaultdict(set)

    def handle_starttag(self, tag, attrs):
        if self._is_category_tag(tag, attrs):
            self._next_data_type = _TagType.CATEGORY
        elif self._is_product_tag(tag, attrs):
            self._next_data_type = _TagType.PRODUCT
        else:
            self._next_data_type = _TagType.OTHER

    def handle_data(self, data):
        if self._next_data_type == _TagType.CATEGORY:
            self._current_category = data.strip()
        elif self._next_data_type == _TagType.PRODUCT:
            self.products[self._current_category].add(data.strip())
        self._next_data_type = _TagType.OTHER

    @classmethod
    def _is_category_tag(cls, tag, attrs) -> bool:
        return tag == 'h2' and cls._has_class(attrs, 'h4')

    @classmethod
    def _is_product_tag(cls, tag, attrs) -> bool:
        return tag == 'h3' and cls._has_class(attrs, 'h5')

    @classmethod
    def _has_class(cls, attrs, classname) -> bool:
        class_attr = cls._get_attr(attrs, 'class')
        if class_attr is None:
            return False
        regex = re.compile(rf"\b{re.escape(classname)}\b")
        return re.search(regex, class_attr) is not None

    @classmethod
    def _get_attr(cls, attrs, attr_name) -> str | None:
        for (key, value) in attrs:
            if key == attr_name:
                return value.strip()
        return None
