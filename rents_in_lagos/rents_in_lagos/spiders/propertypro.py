from types import NoneType
import scrapy
import re

from itemloaders.processors import MapCompose
from scrapy.loader import ItemLoader

from ..items import FileItem

location_list = [
    "Abule Egba",
    "Agege",
    "Ajah",
    "Ajaokuta",
    "Alimosho",
    "Amuwo Odofin",
    "Apapa",
    "Arepo",
    "Badagry",
    "Bariga",
    "Egbe Idimu",
    "Egbeda",
    "Ejigbo",
    "Epe",
    "Gbagada",
    "Ibeju Lekki",
    "Iju",
    "Ikeja",
    "Ikorodu",
    "Ikotun Igando",
    "Ikoyi",
    "Ilaje",
    "Ilupeju",
    "Ipaja",
    "Isolo",
    "Ketu",
    "Kosofe Ikosi",
    "Lagos Island",
    "Lekki",
    "Maryland",
    "Mushin",
    "Ogba",
    "Ogba Egbema Ndoni",
    "Ogudu",
    "Ojo",
    "Ojodu",
    "Ojota",
    "Okota",
    "Orile",
    "Oshodi",
    "Sangotedo",
    "Shagari",
    "Shomolu",
    "Surulere",
    "Victoria Island",
    "Yaba",
]


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
        if "$" in cleaned_price:
            cleaned_price.remove("$")
        locations = response.css(".single-room-sale .single-room-text h4:not([class])::text").extract()

        cleaned_location= []
        for location in locations: 
            if location in UNWANTED_VALUES:
                locations.remove(location)
        for value in locations:
            for loc in location_list:
                if loc in value:
                    cleaned_location.append(value.replace(value,loc))

        for title in titles:
            item = ItemLoader(FileItem(), title)
            title_text = title.css(".listings-property-title::text").extract_first()
            try:
                cleaned_title = re.findall('[0-9]+', title_text)[0]
            except IndexError:
                cleaned_title = 0
            item.add_value("house_type", int(cleaned_title))
            num = titles.index(title)
            item.add_value("price", int(cleaned_price[num]))
            item.add_value("location", cleaned_location[num])
            yield item.load_item()
        # next_page = response.css("a[alt='view next property page']::attr('href')").get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

