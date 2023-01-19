# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

from judge.models import Judge
from movement.models import Movement
from parts.models import Part
from process.models import Process


class CrawlingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProcessItem(DjangoItem):
    django_model = Process


class PartItem(DjangoItem):
    django_model = Part


class MovementItem(DjangoItem):
    django_model = Movement


class JudgeItem(DjangoItem):
    django_model = Judge
