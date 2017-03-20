# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.encoding import python_2_unicode_compatible

from core.utils import SLUG_FIELD_PARAMS, NONUNIQUE_SLUG_FIELD_PARAMS


@python_2_unicode_compatible
class Survey(models.Model):
    # Subclasses must provide a `slug` field
    # slug = models.CharField(...)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    model = JSONField()

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class EventSurvey(Survey):
    event = models.ForeignKey('core.Event')
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    class Meta:
        unique_together = [('event', 'slug')]


class GlobalSurvey(Survey):
    slug = models.CharField(**SLUG_FIELD_PARAMS)
