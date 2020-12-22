# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
import pymongo

from typing import Dict
from itemadapter import ItemAdapter

from google_sheet.services import append_row_in_google_sheet, get_list_data_from_dict
from parsing.utils import create_new_file_with_current_date


class MongoPipeline:

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.list_values = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # Clear collection with last urls parse
        self.db[f'{self.collection_name}_new_urls'].remove()

    def close_spider(self, spider):
        self.client.close()
        list_fields = []
        fields = [
            "url",
            "job_title",
            "employer_name",
            "job_description",
            "job_qualifications",
            "job_posted_date",
            "job_location",
            "job_type",
            "job_sector",
            "job_categories",
            "required_education",
            "about_employer",
        ]
        # list_fields.append(fields)
        # append_row_in_google_sheet(list_fields.append(fields), range='A0',)
        append_row_in_google_sheet(self.list_values, range='A1')
        create_new_file_with_current_date()

    def append_new_items(self, data: Dict):
        self.db[f'{self.collection_name}_new_urls'].insert_one(
            {
                'url': data['url'],
                'date_creation': datetime.datetime.now()
            }
        )
        data_list = get_list_data_from_dict(data)
        self.list_values.append(data_list)

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        if self.db[self.collection_name].count_documents({'url': data['url']}) == 0:
            self.db[self.collection_name].insert_one(data)
            self.append_new_items(data)
        return item
