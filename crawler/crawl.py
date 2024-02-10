import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.phonesList import Phones


def crawl_job():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(Phones)
    process.start()  # the script will block here until the end of the crawl


if __name__ == '__main__':

    while True:
        crawl_job()
        time.sleep(3600)  # 60 * 60 sec =  1 hour  :D
