# -*- coding: utf-8 -*-
import requests
import json
import urlparse
from pyquery import PyQuery as pq
import re


def get_base(parsed_url):

    base_url = parsed_url[0] + '://' + parsed_url[1]
    base_url = base_url.encode('ascii', 'ignore')
    return base_url


def get_exchange_rates():
    ''' return dictionary of exchange rates with british pound as base
        currency '''

    url = 'http://api.fixer.io/latest?base=GBP'
    try:
        response = requests.get(url)
        er = json.loads(response.content)['rates']
        return er
    except:
        return {'error': 'Could not contact server'}


def determine_stock_status(sizes):

    result = {}
    for i in xrange(1, len(sizes)):
        option = sizes.eq(i).text()
        if 'Sold Out' not in option:
            result[option] = 'In Stock'
        else:
            size = option.split(' ')[0]
            result[size] = 'Sold Out'
    return result


def determine_type(short_summary):

    short_summary = short_summary.upper()

    S = (
        'HEEL', 'SNEAKER', 'SNEAKERS',
        'BOOT', 'FLATS', 'WEDGES',
        'SANDALS'
    )

    J = (
        'RING', 'NECKLACE', 'RING',
        'BANGLE', 'CHOKER', 'COLLIER',
        'BRACELET', 'TATTOO', 'EAR JACKET'
    )

    B = (
        'BAG', 'PURSE', 'CLUTCH',
        'TOTE'
    )

    A = (
        'PINNI', 'BLOUSE', 'TOP',
        'SKIRT', 'KNICKER', 'DRESS',
        'DENIM', 'COAT', 'JACKET',
        'SWEATER', 'JUMPER', 'SHIRT',
        'SKINNY', 'SHORT', 'TEE',
        'PANTS', 'JUMPSUIT', 'HIGH NECK',
        'GOWN', 'TROUSER', 'ROBE',
        'PLAYSUIT', 'CULOTTE', 'JODPHUR',
        'PANTALON', 'FLARE', 'CARDIGAN',
        'VEST', 'CAMI', 'BEDSHORT',
        'PYJAMA', 'BRALET', 'TUNIC',
        'HOODY', 'SATEEN', 'BIKER',
        'JEAN', 'SWEAT', 'PULL',
        'BIKINI', 'LE GRAND GARCON'
    )

    types = {
        'B': B, 'S': S,
        'J': J, 'A': A
    }

    for key, val in types.iteritems():
        for t in val:
            if t in short_summary:
                return key
    else:
        return 'R'  # Tag as accessory as failsafe


def fetch_images(image_links, base_url):
    ''' base_url will come as unicode change to python string '''

    images = []

    for image in image_links:
        images.append(urlparse.urljoin(base_url, image.attrib['src']))

    return images


def get_price_and_discount(gbp_price):

    if gbp_price['prices']('.mark').text() == '':  # No discount
        gbp_price['discount'] = '0%'
        orig_price = float(gbp_price['prices'].parent().text()
                           .encode('ascii', 'ignore'))
    else:  # Calculate discount
        prices = gbp_price['prices']
        orig_price = "{0:.2f}".format(float(prices('.mark').text()))
        new_price = "{0:.2f}".format(float(gbp_price['prices'].eq(1).text()))
        gbp_price['discount'] = "{0:.2f}"\
            .format(float(orig_price) / float(new_price) * 100) + '%'
    return float(orig_price), gbp_price['discount']


def get_raw_image_color(image):
    ''' Note that Pillow imaging library would be perfect
        for this task. But external libraries are not
        allowed via the constraints noted in the instructions.
        Example: Image.get_color(image)
        Could be used with Pillow.
    '''

    # only import Pillow image library if this is used
    # Later
    from PIL import Image
    im = Image.open(image)
    colors = im.getcolors()
    if colors is None:
        return None
    else:
        return colors[0]  # Not functional at this point


def get_product_color_from_description(description):
    ''' Will go this route to avoid external imports '''

    description = description.upper().split(' ')
    colors = (
        'BLACK', 'WHITE', 'BLUE',
        'YELLOW', 'ORANGE', 'GREY',
        'PINK', 'FUSCIA', 'RED',
        'GREEN', 'PURPLE', 'INDIGO',
        'VIOLET'
    )

    for word in description:
        for color in colors:
            if word == color:
                return color.lower()
    else:
        return None


def generate_sitemap_rules():

    d = pq(requests.get('http://www.oxygenboutique.com').content)

    # Proof of concept regex can be found here --> http://regexr.com/3c0lc
    designers = d('ul.tame').children()
    re_front = r'(http:\/\/)(www\.)(.+\/)((?!'
    re_back = r').+)'
    re_middle = 'products|newin|product|lingerie|clothing'

    for li in designers:
        ''' This removes 36 requests from the queue '''

        link = pq(li.find('a')).attr('href').rstrip('.aspx')
        re_middle += '|' + link

    return [(re_front + re_middle.replace('-', r'\-') + re_back,
            'parse_sitemap_url')]
