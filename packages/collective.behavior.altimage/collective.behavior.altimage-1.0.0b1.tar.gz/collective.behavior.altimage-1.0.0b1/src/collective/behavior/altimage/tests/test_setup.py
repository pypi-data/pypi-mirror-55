# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.behavior.altimage.testing import COLLECTIVE_BEHAVIOR_ALTIMAGE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.behavior.altimage is properly installed."""

    layer = COLLECTIVE_BEHAVIOR_ALTIMAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])

    def test_product_installed(self):
        """Test if collective.behavior.altimage is installed."""
        self.assertTrue(
            self.installer.is_product_installed('collective.behavior.altimage')
        )

    def test_browserlayer(self):
        """Test that ICollectiveBehaviorAltimageLayer is registered."""
        from collective.behavior.altimage.interfaces import (
            ICollectiveBehaviorAltimageLayer,
        )
        from plone.browserlayer import utils

        self.assertIn(
            ICollectiveBehaviorAltimageLayer, utils.registered_layers()
        )


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_BEHAVIOR_ALTIMAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('collective.behavior.altimage')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.behavior.altimage is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed('collective.behavior.altimage')
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveBehaviorAltimageLayer is removed."""
        from collective.behavior.altimage.interfaces import (
            ICollectiveBehaviorAltimageLayer,
        )
        from plone.browserlayer import utils

        self.assertNotIn(
            ICollectiveBehaviorAltimageLayer, utils.registered_layers()
        )
