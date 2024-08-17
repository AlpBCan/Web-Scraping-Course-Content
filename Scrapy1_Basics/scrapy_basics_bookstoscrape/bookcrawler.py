import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BookItem

number_dict = {'One': '1', 'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5'}

class BookcrawlerSpider(CrawlSpider):
    name = "bookcrawler"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]

    rules = (
        Rule(LinkExtractor(allow='catalogue/page')),
        Rule(LinkExtractor(allow='catalogue', deny=('category', 'page')), callback="parse_item"),
    )
    def parse_item(self, response):
        book = BookItem()

        book['name'] = response.css('div.product_main h1::text').get()
        book['price_exc_tax'] = response.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td/text()').get()
        book['price_inc_tax'] = response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td/text()').get()
        book['upc'] = response.xpath('//th[text()="UPC"]/following-sibling::td/text()').get()
        book['availability'] = response.xpath('//th[text()="Availability"]/following-sibling::td/text()').get()
        book['tax'] = response.xpath('//th[text()="Tax"]/following-sibling::td/text()').get()

        category_children = response.xpath('//ul[@class="breadcrumb"]/child::*')
        book['category'] = category_children[2].css('a::text').get()

        star_tag = response.css('p.star-rating')
        class_name_string = star_tag.attrib['class']
        # One
        stars = class_name_string.split(' ')[-1]
        book['stars'] = number_dict[stars]

        book['image_url'] = 'https://books.toscrape.com' + response.css('div.active img').attrib['src'][5:]

        yield book
