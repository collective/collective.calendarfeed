"""

    Settings for collective.calendarfeed

"""

from zope import schema
from five import grok

# grok CodeView is now View
try:
    from five.grok import CodeView as View
except ImportError:
    from five.grok import View

from Products.CMFCore.interfaces import ISiteRoot

from z3c.form.browser.checkbox import CheckBoxFieldWidget


from plone.z3cform import layout
from plone.directives import form
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from zope.i18nmessageid import MessageFactory

_ = MessageFactory("collective.calendarfeed")

class ISettings(form.Schema):
    """ Define settings data structure """
    google_apikey = schema.TextLine(title=_(u"Google API Key"),
    description=_(u"Add your Google issued API key. For more information visit: https://developers.google.com/google-apps/calendar/auth"),
        required=True)
    calendar_address = schema.TextLine(title=_(u"Calendar Address"),
    description=_(u"This is usually in the form of an email address associated with a public Google Calendar"),
         required=True)
    

class SettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = ISettings
    label = _(u"Collective Calendarfeed View settings")


class SettingsView(View):
    """

    """
    grok.name("calendarfeed-settings")
    grok.context(ISiteRoot)
    grok.require("cmf.ManagePortal")

    def render(self):
        view_factor = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()
