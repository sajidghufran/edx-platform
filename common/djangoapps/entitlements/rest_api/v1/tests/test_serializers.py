"""
Tests for the API Serializers.
"""

import unittest

from django.conf import settings
from django.test import RequestFactory

from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase

# Entitlements is not in CMS' INSTALLED_APPS so these imports will error during test collection
if settings.ROOT_URLCONF == 'lms.urls':
    from entitlements.rest_api.v1.serializers import CourseEntitlementSerializer
    from entitlements.tests.factories import CourseEntitlementFactory


@unittest.skipUnless(settings.ROOT_URLCONF == 'lms.urls', 'Test only valid in lms')
class EntitlementsSerializerTests(ModuleStoreTestCase):
    """
    Tests for the Entitlement Serializers.
    """

    def test_data(self):
        entitlement = CourseEntitlementFactory()
        request = RequestFactory().get('')
        serializer = CourseEntitlementSerializer(entitlement, context={'request': request})

        expected = {
            'user': entitlement.user.username,
            'uuid': str(entitlement.uuid),
            'expired_at': entitlement.expired_at,
            'course_uuid': str(entitlement.course_uuid),
            'mode': entitlement.mode,
            'refund_locked': False,
            'order_number': entitlement.order_number,
            'created': entitlement.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'modified': entitlement.modified.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'support_details': [],
        }

        assert serializer.data == expected
