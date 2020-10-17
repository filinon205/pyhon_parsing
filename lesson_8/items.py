# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    photo = scrapy.Field()
    likes = scrapy.Field()
    post = scrapy.Field()

    _id = scrapy.Field()

    follower_id = scrapy.Field()
    follower_name = scrapy.Field()
    follower_full_name = scrapy.Field()
    follower_photo = scrapy.Field()
    follower = scrapy.Field()

    subscription_id = scrapy.Field()
    subscription_name = scrapy.Field()
    subscription_full_name = scrapy.Field()
    subscription_photo = scrapy.Field()
    subscription = scrapy.Field()