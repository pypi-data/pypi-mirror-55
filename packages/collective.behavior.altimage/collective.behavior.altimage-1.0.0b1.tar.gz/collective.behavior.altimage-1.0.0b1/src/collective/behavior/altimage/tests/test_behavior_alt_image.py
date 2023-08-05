# -*- coding: utf-8 -*-
from collective.behavior.altimage.behavior import IAltImageMarker
from collective.behavior.altimage.testing import COLLECTIVE_BEHAVIOR_ALTIMAGE_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class AltImageIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_BEHAVIOR_ALTIMAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_altimage(self):
        behavior = getUtility(IBehavior, 'collective.behavior.altimage')
        self.assertEqual(behavior.marker, IAltImageMarker)
        behavior_name = 'collective.behavior.altimage.behavior.IAltImage'
        behavior = getUtility(IBehavior, behavior_name)
        self.assertEqual(behavior.marker, IAltImageMarker)
