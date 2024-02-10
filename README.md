Crawler Project
Overview

This project is a web crawler developed with Python and Scrapy. It is designed to extract data from websites efficiently and store it in a structured format. The main goal of this crawler is to gathering mobile phone's prices.

Prerequisites

    Python 3.x
    Scrapy

Ensure Python and Scrapy are installed on your system. If not, you can install Scrapy using pip:

bash

pip install scrapy

Installation

To get started with this project, clone this repository to your local machine:

bash

git clone https://github.com/amir-rze/Information-retrieval-Crawler-Scrapy.git

Navigate to the project directory:

bash

cd crawler_project

Usage

To run the crawler, use the following command:

bash

scrapy crawl [name_of_your_spider]


Configuration

    Settings.py: Configure project-wide settings such as USER_AGENT, CONCURRENT_REQUESTS, and ITEM_PIPELINES here.
    Spiders/: This directory contains all your spider scripts. You can customize or add new spiders as needed.


Remember to change the database fields according to your needs.
