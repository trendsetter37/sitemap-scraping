# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders.sitemap import *
from pyquery import PyQuery as pq
from oxygendemo.items import OxygendemoItem
import oxygendemo.utilities
from oxygendemo.utilities import *


class OxygenSpider(SitemapSpider):

    print 'MY SPIDER, IS ALIVE'
    name = "oxygen"
    allowed_domains = ["oxygenboutique.com"]
    sitemap_urls = ['http://www.oxygenboutique.com/sitemap.xml']
    sitemap_rules = generate_sitemap_rules()
    ex_rates = get_exchange_rates()

    def parse_sitemap_url(self, response):

        self.logger.info('Entered into parse_sitemap_url method')
        self.logger.info('Received response from: {}'.format(response.url))
        self.logger.debug('Respons status: {}'.format(response.status))

        item = OxygendemoItem()
        d = pq(response.body)
        parsed_url = urlparse.urlparse(response.url)
        base_url = get_base(parsed_url)
        product_info = d('.right div#accordion').children()
        image_links = d('div#product-images tr td a img')
        description = product_info.eq(1).text()\
            .encode('ascii', 'ignore')
        item['code'] = str(parsed_url[2].lstrip('/')[:-5])
        item['description'] = description
        item['link'] = parsed_url.geturl()
        item['name'] = d('.right h2').text()

        gbp_price = {
            'prices': d('.price').children(),
            'discount': 0
            }

        item['gbp_price'], item['sale_discount'] = get_price_and_discount(
            gbp_price
        )

        if 'error' not in self.ex_rates:

            item['usd_price'] = "{0:.2f}".format(
                item['gbp_price'] * self.ex_rates['USD']
                )
            item['eur_price'] = "{0:.2f}".format(
                item['gbp_price'] * self.ex_rates['EUR']
                )
        else:

            item['usd_price'], item['eur_price'] = ['N/A'] * 2

        item['designer'] = d('.right').find('.brand_name a').text()
        item['stock_status'] = json.dumps(determine_stock_status(d('select')
                                          .children()))
        item['gender'] = 'F'  # Oxygen boutique carries Womens's clothing
        item['image_urls'] = fetch_images(image_links, base_url)
        item['raw_color'] = get_product_color_from_description(description)

        yield item
