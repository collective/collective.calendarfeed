from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.i18nmessageid import MessageFactory

_ = MessageFactory("collective.fullcalendarioview")

#from plone.portlet.static import PloneMessageFactory as _

# Import the base portlet module whose properties we will modify
# from plone.portlet.static import static
from .portlet_edit import AddForm,Assignment,IGoogleCalendarFeedPortlet,Renderer

#class IGoogleCalendarFeedPortlet(IStaticPortlet):
#    """ Defines a new portlet "Google Calendar Feed" which takes properties of the existing static text portlet. """
#    pass

class GoogleCalendarFeedRenderer(Renderer):
    """ Overrides static.pt in the rendering of the portlet. """
    render = ViewPageTemplateFile('portlet_google_calendar_feed.pt')

class GoogleCalendarFeedAssignment(Assignment):
    """ Assigner for google_calendar_feed static portlet. """
    implements(IGoogleCalendarFeedPortlet)

class GoogleCalendarFeedAddForm(AddForm):
    """ Make sure that add form creates instances of our custom portlet instead of the base class portlet. """
    def create(self, data):
        return GoogleCalendarFeedAssignment(**data)
