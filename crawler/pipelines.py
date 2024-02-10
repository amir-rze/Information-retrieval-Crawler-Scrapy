# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from decouple import config
import psycopg2


class CrawlerPipeline(object):

    def open_spider(self, spider):
        hostname = config('DATABASE_HOST')
        username = config('DATABASE_USER')
        password = config('DATABASE_PASSWORD')
        database = config('DATABASE_NAME')
        self.connection = psycopg2.connect(host=hostname, user=username,
                                           password=password, dbname=database)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        print("processing item")
        self.store_item(item)
        return item

    def store_item(self, item):
        print("storing data")
        try:
            if item['name']:
                name = "'" + item['name'] + "'" if item['name'] is not None else ' '
                self.cursor.execute("select COUNT(*) from phones where name = {} ;".format(name))
                count = self.cursor.fetchone()
            else:
                count = [0, ]
            if count[0] == 0:
                self.cursor.execute(
                    "insert into phones(name,title,max_price,min_price,link ) values(%s,%s,%s,%s,%s)",
                    (item['name'], item['title'], item['max_price'],
                     item['min_price'], item['link']))
            else:
                print("replacing")
                link = "'" + item['link'] + "'" if item['link'] is not None else 'null'
                title = "'" + item['title'] + "'" if item['title'] is not None else 'null'
                name = "'" + item['name'] + "'" if item['name'] is not None else 'null'
                max_price = "'" + item['max_price'] + "'" if item['max_price'] is not None else 'null'
                min_price = "'" + item['min_price'] + "'" if item['min_price'] is not None else 'null'
                self.cursor.execute(
                    f"update phones set title = {title} ,max_price = {max_price},min_price = {min_price} , link = {link} where name = {name}")
        except:
            print("rollbacking")
            self.cursor.execute("rollback;")
        self.connection.commit()

    # def store_item(self, item):
    #     self.cursor.execute(
    #         "insert into phones(name,title,max_price,min_price,link ) values(%s,%s,%s,%s,%s)",
    #         (item['name'], item['title'], item['max_price'],
    #          item['min_price'], item['link']))
    #     self.connection.commit()
