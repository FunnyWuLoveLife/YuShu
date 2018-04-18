#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/10 1:17
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import current_app as app
from bs4 import BeautifulSoup

from util.httpHelper import HTTP

from ..models.book import BookModel


class DouBanBook:
    # _isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    _isbn_url = 'https://api.douban.com/v2/book/isbn/{}'
    # _keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'
    _keyword_url = 'https://api.douban.com/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        book = BookModel.find_book_by_isbn(isbn)
        if book:
            self._fill_single(book)
        else:
            result = HTTP.get(self._isbn_url.format(isbn))
            if result.get('title', None) and result.get('code', '') != 6000:
                if result.get('isbn13'):
                    result['isbn'] = result.get('isbn13')
                elif result.get('isbn10'):
                    result['isbn'] = result.get('isbn10')
                print('douban', result)
                BookModel().set_attrs_from_douban(result).save()
                self._fill_single(result)
            else:
                book = JdSpider.search(isbn)
                BookModel().set_attrs(book).save()
                self._fill_single(book)
        return self

    def _fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

        return self

    def _fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']
        return self

    def search_by_keyword(self, keyword, page=1):
        url = self._keyword_url.format(keyword,
                                       app.config['PRE_PAGE'],
                                       self.calculate_start(page))
        result = HTTP.get(url)
        if result:
            res = []
            for book in result.get('books', list()):
                if book.get('isbn13'):
                    book['isbn'] = book.get('isbn13')
                    BookModel().set_attrs_from_douban(book).save()
                    res.append(book)
                elif book.get('isbn10'):
                    book['isbn'] = book.get('isbn13')
                    BookModel().set_attrs_from_douban(book).save()
                    res.append(book)
            result['books'] = res
        self._fill_collection(result)
        return self

    @classmethod
    def calculate_start(cls, page):
        return (page - 1) * app.config['PRE_PAGE']

    @property
    def first(self):
        if self.total >= 1:
            return self.books[0]
        else:
            return None


class JdSpider:
    _search_url = "https://search.jd.com/Search?keyword={}" \
                  "&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=9787560639192&wtype=1"

    @classmethod
    def search(cls, isbn):
        html = HTTP.get(cls._search_url.format(isbn), return_json=False)

        url = cls.get_url(html)
        return cls.get_book(url)

    @classmethod
    def get_url(cls, text):
        soup = BeautifulSoup(text, 'html.parser')
        div = soup.find('div', {'class': 'p-name'})
        a = div.a if div else None
        url = a.get('href') if a else ''
        if url.startswith('//'):
            url = 'https:' + url
        return url

    @classmethod
    def get_book(cls, url):
        html = HTTP.get(url, return_json=False)
        if html:
            book = {
                'title': '',
                'author': [],
                'binding': '',
                'category': '',
                'image': [],
                'isbn': '',
                'pages': 0,
                'price': '未知',
                'pubdate': '',
                'publisher': '',
                'summary': '',
            }
            soup = BeautifulSoup(html, 'html.parser')

            # 图片
            image_div = soup.find('div', {'class': 'main-img'})
            image = image_div.find('img') if image_div else None
            image_url = image.get('src') if image else ''
            image_url = 'https:' + image_url if image_url.startswith('//') else image_url
            book['image'] = image_url if image_url else 'https://yushu.xbc922.com/static/images/no_image.png'

            # 书名
            title = soup.find('div', {'class': 'sku-name'})
            title_text = title.text if title else ''
            book['title'] = title_text[:title_text.index('/')] if '/' in title_text else title_text

            # 作者
            p_author = soup.find('div', {'id': 'p-author'})
            a_author = p_author.a if p_author else None
            book['author'] = [a_author.get('data-name', '')]

            # p-parameter-list
            ul = soup.find('ul', {'class': 'p-parameter-list'})
            lis = ul.find_all('li') if ul.find('li') else []
            for li in lis:
                if 'ISBN' in li.text:
                    book['isbn'] = li.get('title')
                    continue
                if '出版社' in li.text:
                    book['publisher'] = li.get('title')
                    continue
                if '包装' in li.text:
                    book['binding'] = li.get('title')
                    continue
                if '出版时间' in li.text:
                    book['pubdate'] = li.get('title')[:-3]
                    continue
                if '页数' in li.text:
                    book['pages'] = li.get('title')
                    continue
            return book
        else:
            return None
