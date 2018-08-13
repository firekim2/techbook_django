#-*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from .utility import load_json
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
import datetime

base_url = 'localhost'


def main_upload_directory(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ('main_img', ext)
    return 'techbook/{0}/{1}'.format(instance.edition, filename)

def calender_upload_directory(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ('calender', ext)
    return 'techbook/{0}/{1}'.format(instance.edition, filename)


class Versions(models.Model):
    version_a = models.CharField(max_length=5, blank=True)
    version_i = models.CharField(max_length=5, blank=True)
    published_date = models.DateTimeField(primary_key=True, default=timezone.now)

    def __str__(self):
        return 'android : ' + self.version_a + ', ios : ' + self.version_i

    def json_version_a(self):
        return {'version': self.version_a}

    def json_version_i(self):
        return {'version': self.version_i}


class Editions(models.Model):
    publish = models.BooleanField(default=False)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    edition = models.PositiveIntegerField(primary_key=True)
    img = models.ImageField(upload_to=main_upload_directory, blank=False)
    calender = models.ImageField(upload_to=calender_upload_directory, blank=True, null=True)
    calender_thumbnail = ImageSpecField(
                source = 'calender',
                processors = [Thumbnail(362, 512)],
                format = 'JPEG',
                options = {'quality' : 60})

    def __str__(self):
        return "edition " + str(self.edition)

    def json_edition(self):
        return {'edition_year': self.year,
                'edition_number': str(self.edition),
                'edition_month': self.month,
                'edition_cover': base_url + self.img.url}

    def json_calender(self):
        return {'year' : self.year,
                'month' : self.month,
                'calender' : base_url + self.calender.url,
                'calender_thumbnail' : base_url + self.calender_thumbnail.url}


class Articles(models.Model):
    guest = models.BooleanField(default=False)
    categories = ['테크토크', '테크피플', '못보던 프로토타입']
    categories_season_1 = ['못보던 기술', '못보던 기술회사', '못보던 프로토타입']
    ARTICLE_CHOICES = (
        (0, categories[0]),
        (1, categories[1]),
        (2, categories[2]),
    )
    category = models.PositiveIntegerField(default=0, choices=ARTICLE_CHOICES)
    title = models.CharField(max_length=100, default='title', blank=False)
    edition = models.PositiveIntegerField(default=0, blank=False)
    view_count = models.PositiveIntegerField(default=0)
    content = models.TextField(default=[], blank=False)
    tag = models.CharField(max_length=10 * 21, default='', blank=False)

    def __str__(self):
        return str(self.edition) + ' - ' + self.categories[self.category] + ' : ' + self.title

    def update_view_count(self):
        self.view_count += 1
        self.save()

    def json_list(self):
        if self.edition < 7:
            self.categories = self.categories_season_1
        return {'article_category': self.categories[self.category],
                'article_title': self.title,
                'article_tag' : self.title + ', ' + self.tag,
                'article_address' : str(self.edition) + '_' + str(self.category)}

    def json_content(self):
        if self.edition < 7:
            self.categories = self.categories_season_1
        return {'edition' : self.edition,
        'category' : self.categories[self.category],
        'category_no' : self.category,
        'title': self.title,
        'content': load_json(self.content)}


class Messages(models.Model):
    name = models.CharField(max_length=20, default='noname')
    message = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    check = models.BooleanField(default=False)

    def __str__(self):
        return str(self.time.year) + '-' + str(self.time.month) + '-' + str(self.time.day) + ' : ' + self.name


class Notices(models.Model):
    content = models.TextField()
    publish_date = models.DateField(blank=False, null=False, default=datetime.date.today)
    expire_date = models.DateField(blank=False, null=False, default=datetime.date.today() + datetime.timedelta(days=7))

    def __str__(self):
        return self.content + str(self.is_valid())

    def notice_json(self):
        return {'result_msg': 'Y', 'content': self.content}

    def is_valid(self):
        valid = (self.expire_date - datetime.date.today()).days > 0\
                and (datetime.date.today() - self.publish_date).days >= 0
        return valid


class Guests(models.Model):
    client = models.CharField(max_length=20)
    id = models.CharField(max_length=20, primary_key=True)
    pw = models.CharField(max_length=20)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.client + ' : ' + self.id

    def view_count_up(self):
        self.view_count += 1
