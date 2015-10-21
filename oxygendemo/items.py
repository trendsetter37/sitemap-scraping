# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class OxygendemoItem(scrapy.Item):

    code = Field()  # unique identifier (retailers perspective)
    description = Field()  # Detailed description
    designer = Field()  # manufacturer
    eur_price = Field()  # full (non_discounted) price
    gender = Field()  # F - Female, M - male
    gbp_price = Field()  # full (non_discounted) price
    image_urls = Field()  # list of urls representing the item
    link = Field()  # url of product page
    name = Field()  # short summary of the item
    raw_color = Field()  # best guess of color. Default = None
    sale_discount = Field()  # % discount for sale item where applicable
    stock_status = Field()  # dictionary of sizes to stock status
    '''
                   size: quantity
        Example: { 'L': 'In Stock',
                   'M': 'In Stock',
                   'S': 'In Stock',
                   'XS': 'In Stock'
                 }
    '''
    # 'A' = apparel, 'B' = bags, 'S' = shoes, 'J' = jewelry, 'R' = accessories
    type = Field()
    usd_price = Field()  # full (non_discounted) price
