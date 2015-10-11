# encoding: utf-8

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from core.helpers import person_required
from core.models import Organization
from core.utils import initialize_form

from ..helpers import membership_organization_required
from ..models import Membership
from ..forms import MembershipForm


@membership_organization_required
@person_required
def membership_apply_view(request, organization):
    mandatory_information_missing = not (
        request.user.person and
        request.user.person.first_name and
        request.user.person.surname and
        request.user.person.muncipality and
        request.user.person.email
    )
    already_member = Membership.objects.filter(
        organization=organization,
        person=request.user.person,
    ).exists()

    can_apply = (not mandatory_information_missing) and (not already_member)

    form = initialize_form(MembershipForm, request)

    if request.method == 'POST':
        if already_member:
            messages.error(request, u'Olet jo jäsen tai jäsenhakemuksesi on jo käsiteltävänä.')
        elif mandatory_information_missing:
            messages.error(request, u'Profiilistasi puuttuu pakollisia tietoja.')
        elif not form.is_valid():
            messages.error(request, u'Tarkista lomakkeen tiedot.')
        else:
            membership = form.save(commit=False)
            membership.organization = organization
            membership.person = request.user.person
            membership.state = 'approval'
            membership.save()

            messages.success(request,
                u'Kiitos jäsenyyshakemuksestasi! Yhdistyksen hallitus käsittelee '
                u'hakemuksesi seuraavassa kokouksessaan.'
            )

        return redirect('core_organization_view', organization.slug)

    vars = dict(
        form=form,
        organization=organization,
        meta=organization.membership_organization_meta,
        mandatory_information_missing=mandatory_information_missing,
        already_member=already_member,
        can_apply=can_apply,
    )

    return render(request, 'membership_apply_view.jade', vars)


@person_required
def membership_profile_view(request):
    memberships = Membership.objects.filter(person=request.user.person)
    potential_organizations = Organization.objects.filter(
        membershiporganizationmeta__receiving_applications=True,
    ).exclude(
        members__person=request.user.person,
    )

    vars = dict(
        memberships=memberships,
        potential_organizations=potential_organizations,
    )

    return render(request, 'membership_profile_view.jade', vars)


def membership_organization_box_context(request, organization):
    meta = organization.membership_organization_meta
    if not meta:
        return dict()

    if request.user.is_anonymous() or not request.user.person:
        can_apply = True
        membership = None
    else:
        membership = Membership.objects.filter(
            organization=organization,
            person=request.user.person,
        ).first()

    return dict(
        can_apply=meta.receiving_applications and not membership,
        membership=membership,
    )


def membership_profile_menu_items(request):
    membership_profile_url = reverse('membership_profile_view')
    membership_profile_active = request.path.startswith(membership_profile_url)
    membership_profile_text = u'Yhdistysten jäsenyydet'

    return [(membership_profile_active, membership_profile_url, membership_profile_text)]
