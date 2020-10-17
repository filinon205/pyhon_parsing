
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
#from scrapy.pipelines.images import ImagesPipeline

class instaPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.instagram_base

    def process_item(self, item, spider):
        item = ItemAdapter(item)

        # распределяем  item по коллекциям:

        if item.get('likes'):
            collection = self.mongo_base[spider.name + 'post']
            collection.insert_one(item)
            print("New post")

        elif item.get('follower_id'):
            collection = self.mongo_base[spider.name + 'follower']
            collection.insert_one(item)
            print("New follower")

        elif item.get('subscription_id'):
            collection = self.mongo_base[spider.name + 'subscription']
            collection.insert_one(item)
            print("New follower")

        return item