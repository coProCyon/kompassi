# encoding: utf-8

import logging

from django.test import TestCase

from core.models import Person
from labour.models import LabourEventMeta, Signup
from programme.models import ProgrammeEventMeta, Programme, ProgrammeRole

from .models import BadgesEventMeta, Badge


logger = logging.getLogger('kompassi')


class BadgesTestCase(TestCase):
    def setUp(self):
        self.meta, unused = BadgesEventMeta.get_or_create_dummy()
        LabourEventMeta.get_or_create_dummy()
        ProgrammeEventMeta.get_or_create_dummy()

        self.event = self.meta.event
        self.person, unused = Person.get_or_create_dummy()

    def test_condb_423(self):
        """
        Even though a worker has requested to only show their nick or first name on their badge,
        some events have decided that the real name must always be visible.
        """
        self.person.preferred_name_display_style = 'nick'
        self.person.save()

        assert self.person.first_name not in self.person.display_name
        assert self.person.surname not in self.person.display_name

        signup, unused = Signup.get_or_create_dummy()
        signup.job_categories_accepted = signup.job_categories.all()
        signup.personnel_classes.add(signup.job_categories.first().personnel_classes.first())
        signup.state = 'accepted'
        signup.save()

        badge, unused = Badge.get_or_create(event=self.event, person=self.person)

        assert not badge.is_first_name_visible
        assert not badge.is_surname_visible

        self.meta.real_name_must_be_visible = True
        self.meta.save()

        assert badge.is_first_name_visible
        assert badge.is_surname_visible

    def test_condb_137(self):
        p_role, unused = ProgrammeRole.get_or_create_dummy()
