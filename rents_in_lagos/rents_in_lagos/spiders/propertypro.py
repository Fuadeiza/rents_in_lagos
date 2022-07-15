from types import NoneType
import scrapy
import re
import ast

from itemloaders.processors import MapCompose
from scrapy.loader import ItemLoader

from ..items import FileItem

geo_location_list = {
    "Abule Egba": [6.619413,3.510454],
    "Agege": [6.615356, 3.323782],
    "Ajah": [6.466667,3.566667],
    "Alimosho": [6.546609,3.238251],
    "Amuwo Odofin" : [6.429173,3.288546],
    "Apapa": [6.4499982, 3.3666652],
    "Arepo": [6.465422,3.406448],
    "Badagry": [6.416667,2.883333],
    "Bariga": [6.533333,3.383333],
    "Egbe Idimu": [6.453056,3.395833],
    "Egbeda":[6.591947,3.289574],
    "Epe":[6.583333,3.983333],
    "Gbagada":[6.542983,3.392753],
    "Ibeju Lekki": [6.496267,3.596457],
    "Iju": [6.63656, 3.323811],
    "Ikeja": [6.605874,3.349149],
    "Ikorodu": [6.616865,3.508072],
    "Ikotun Igando": [6.59618941675, 3.35544653886],
    "Ikoyi": [6.454812,3.434691],
    "Ilaje": [6.531267, 3.394722],
    "Ilupeju": [6.553648,3.356674],
    "Ipaja": [6.610044,3.289408],
    "Isolo": [6.529962,3.331985],
    "Ketu": [6.606967,3.381726],
    "Kosofe Ikosi": [6.6074,3.38462],
    "Lagos Island": [6.4499982, 3.3999984],
    "Lekki": [6.458985, 3.601521],
    "Maryland": [6.576421,3.365344],
    "Mushin": [6.5333312, 3.3499986],
    "Ogba": [6.632478,3.341067],
    "Ogudu" : [6.580166,3.386174],
    "Ojo": [6.4666648, 3.1833326],
    "Ojodu": [6.625822, 3.354006],
    "Ojota" : [6.578976,3.38542],
    "Okota": [6.508835,3.313712],
    "Orile": [6.630914,3.316181],
    "Oshodi": [6.514193, 3.308678],
    "Sangotedo": [6.453056,3.395833],
    "Shomolu": [6.532954, 3.36739],
    "Surulere": [6.500000, 3.350000],
    "Victoria Island": [6.431111,3.415833],
    "Yaba": [6.50837,3.384247]
}


class PropertyproSpider(scrapy.Spider):
    name = "propertypro"
    allowed_domains = ["www.propertypro.ng"]
    start_urls = ["https://www.propertypro.ng/property-for-rent/in/lagos"]

    def parse(self, response):
        # infos = response.css(".single-room-sale .single-room-text")
        UNWANTED_VALUES = ["Premium Gold", "Sponsored", "Premium"]
        cleaned_price = []
        titles = response.css(".single-room-sale .single-room-text")
        prices = response.css(".single-room-sale .single-room-text h3 span[content!='NGN']::text").extract()
        # clean prices

        cleaned_price = [price.split("/")[0].replace(",","") for price in prices ] 
        for value in cleaned_price:
            if "$" in str(value):
                print(value)
                val = value.replace("$","0")
                val = int(val)
                i = cleaned_price.index(value)
                cleaned_price = cleaned_price[:i]+[int(val)]+cleaned_price[i+1:]
        locations = response.css(".single-room-sale .single-room-text h4:not([class])::text").extract()

        cleaned_location= []
        for location in locations: 
            if location in UNWANTED_VALUES:
                locations.remove(location)
        for value in locations:
            for loc in list(geo_location_list.keys()):
                if loc in value:
                    location_str = value.replace(value,str(geo_location_list[loc]))
                    cleaned_location.append(ast.literal_eval(location_str))


        for title in titles:
            item = ItemLoader(FileItem(), title)
            title_text = title.css(".listings-property-title::text").extract_first()
            try:
                cleaned_title = re.findall('[0-9]+', title_text)[0]
            except IndexError:
                cleaned_title = 0
            try:
                item.add_value("house_type", int(cleaned_title))
                num = titles.index(title)
                item.add_value("price", int(cleaned_price[num]))
                item.add_value("latitude", cleaned_location[num][0])
                item.add_value("longitude", cleaned_location[num][1])
                yield item.load_item()
            except IndexError:
                pass
        next_page = response.css("a[alt='view next property page']::attr('href')").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


