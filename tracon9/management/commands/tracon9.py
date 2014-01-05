# encoding: utf-8

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from core.models import Event, Venue
from labour.models import EventMeta
from ...models import SignupExtra

class Command(BaseCommand):
    args = ''
    help = 'Setup tracon9 specific stuff'

    def handle(*args, **options):
    	venue, unused = Venue.objects.get_or_create(name="Tampere-talo")
    	content_type = ContentType.objects.get_for_model(SignupExtra)
    	event, unused = Event.objects.get_or_create(slug="tracon9", defaults=dict(
    		name="Tracon 9",
    		venue=venue
    	))
    	event_meta, unused = EventMeta.objects.get_or_create(event=event, defaults=dict(
    		signup_extra_content_type=content_type
    	))