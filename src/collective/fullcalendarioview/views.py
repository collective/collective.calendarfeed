import csv
import os
import random
import shutil
import string
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as \
    render_template
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("collective.fullcalendarioview")


class CalendarView(BrowserView):
    """@@ep-result-view"""
    template = render_template('calendar.pt')

    def hello(self):
        return "world"

    def __call__(self):
        self.nothingyet = "Nothing Yet"
        # available in the template
        # as view/summary
        return self.template()
