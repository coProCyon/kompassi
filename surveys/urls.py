# encoding: utf-8

from django.conf.urls import url

from .views import survey_view


urlpatterns = [
    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/surveys/(?P<survey_slug>[a-z0-9-]+)/?$',
        survey_view,
        name='event_survey_view',
    ),

    url(
        r'^surveys/(?P<survey_slug>[a-z0-9-]+)/?$',
        survey_view,
        dict(event_slug=''),
        name='global_survey_view',
    )
]
