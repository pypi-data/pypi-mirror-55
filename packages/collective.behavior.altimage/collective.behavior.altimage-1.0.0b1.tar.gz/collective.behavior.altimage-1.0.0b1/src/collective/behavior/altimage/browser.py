# -*- coding: utf-8 -*-
from collective.behavior.altimage.behavior import IAltImage
from plone.app.layout.viewlets import ViewletBase


class AltImageViewlet(ViewletBase):
    """ A simple viewlet which renders altimage """

    def update(self):
        context = IAltImage(self.context)
        self.available = True if context.altimage else False
