import re
import uuid
import datetime
from flask import url_for
from peewee import *
from app import db
import unicodedata

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

