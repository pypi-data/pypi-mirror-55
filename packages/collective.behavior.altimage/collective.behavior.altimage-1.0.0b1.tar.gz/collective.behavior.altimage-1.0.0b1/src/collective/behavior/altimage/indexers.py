# -*- coding: utf-8 -*-
from .behavior import IAltImage
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.decorator import indexer


@indexer(IDexterityContent)
def has_alt_image(obj):
    """Does the object have an altimage?

    Similar to getIcon from plone.app.contenttypes.
    """
    try:
        obj = IAltImage(obj)
    except TypeError:
        # could not adapt.
        return False
    if obj.altimage:
        return True
    return False
