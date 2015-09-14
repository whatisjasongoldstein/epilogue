import os
import re
import requests
import datetime
import unicodedata
import lxml.html

from flask import url_for
from peewee import *

from .app import db, app

class Document(db.Model):
    draft_id = IntegerField()
    title = CharField()
    slug = CharField()
    content = TextField()
    content_html = TextField()
    draftin_user_id = IntegerField()
    draftin_user_email = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    last_synced_at = DateTimeField(default=datetime.datetime.now)
    date_published = DateTimeField()

    def __unicode__(self):
        return self.title or self.draft_id

    @property
    def readable_date_published(self):
        if self.date_published:
            return datetime.datetime.strftime(self.date_published, "%B %d, %Y")

    def save(self, *args, **kwargs):
        if not self.date_published:
            self.date_published = datetime.datetime.now()

        if not self.slug:
            # Borrowed from Django's slugify
            slug = unicodedata.normalize('NFKD', self.title).encode('ascii', 'ignore').decode('ascii')
            slug = re.sub('[^\w\s-]', '', slug).strip().lower()
            slug = re.sub('[-\s]+', '-', slug)
            self.slug = slug

        return super(Document, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return url_for('post', slug=self.slug)

    def download_images(self):
        tree = lxml.html.fragment_fromstring(self.content_html, create_parent="div")
        images = tree.xpath("//img[@src]")
        for img in images:
            src = img.attrib["src"]
            resp = requests.get(src)

            filename = resp.headers.get("x-file-name")
            directory = os.path.join("media/images", str(self.id))
            
            file_path = os.path.join(app.static_folder, directory, filename)
            file_url = "/".join([app.static_url_path, directory, filename])

            # Update the content
            self.content = self.content.replace(src, file_url)
            self.content_html = self.content_html.replace(src, file_url)

            # If this item exists, skip it
            if os.path.exists(file_path):
                continue

            # Download the file
            directory = os.path.join(app.static_folder, directory)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_path, "wb") as f:
                f.write(resp.content)
                f.close()

        self.save()
