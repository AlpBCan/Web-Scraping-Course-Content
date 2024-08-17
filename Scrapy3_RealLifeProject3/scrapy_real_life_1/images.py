import scrapy
from ..items import TigerItem, ImageItem


class ImageSpider(scrapy.Spider):
    name = "image"
    allowed_domains = ["flyingtiger.com"]
    start_urls = ["https://flyingtiger.com/collections/shop-all"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'tiger.pipelines.JsonWriterPipeline': 10,
            'tiger.pipelines.CustomImagesPipeline': 20,
        },
        'IMAGES_STORE': 'tiger_images'
    }

    def parse(self, response):
        container = response.css('ul#product-grid')
        items_a_tags = container.css('a.card__information--title')

        for a_tag in items_a_tags:
            product_url = 'https://flyingtiger.com' + a_tag.attrib['href']
            yield scrapy.Request(product_url, callback=self.parse_items)

        next_page_link = response.css('a[aria-label="Next"]')

        if next_page_link:
            yield response.follow(next_page_link.attrib['href'], callback=self.parse)

    def parse_items(self, response):
        tiger_item = TigerItem()

        tiger_item['name'] = response.css('h1.title::text').get().strip()
        tiger_item['price'] = response.css('span.price-item::text').get().strip()
        # Product code: 3059034
        tiger_item['product_code'] = response.css('div.product__sku::text').get().split(':')[-1].strip()
        # //flyingtiger.com/cdn/shop/files/tumbler-with-lid-and-straw-12-l-kitchen-flying-tiger-copenhagen-989640.jpg?v=1717051519&width=1200
        tiger_item['image_url'] = ('https:' +
                                   response.css('div.product__media img').attrib['src'].split('?')[0])
        tiger_item['product_url'] = response.url

        yield tiger_item

        image_item = ImageItem()

        image_item['image_url'] = ('https:' +
                                   response.css('div.product__media img').attrib['src'].split('?')[0])

        image_item['product_code'] = response.css('div.product__sku::text').get().split(':')[-1].strip()

        yield image_item
