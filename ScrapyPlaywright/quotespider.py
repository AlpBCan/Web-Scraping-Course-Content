from typing import Iterable

import scrapy
from scrapy import Request
from ..items import QuoteItem


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"

    def start_requests(self):
        yield scrapy.Request('http://quotes.toscrape.com/js/', meta={"playwright": True})

    def parse(self, response):
        quotes = response.css('div.quote')

        for quote in quotes:
            quote_item = QuoteItem()
            quote_item['quote'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            tags_string = ''
            tags = quote.css('a.tag::text').getall()
            for tag in tags:
                tags_string += tag + ' '
            quote_item['tags'] = tags_string.strip()

            yield quote_item

        next_button_link = response.css('li.next a::attr(href)').get()
        if next_button_link is not None:
            yield response.follow(next_button_link, callback=self.parse, meta={"playwright": True})
