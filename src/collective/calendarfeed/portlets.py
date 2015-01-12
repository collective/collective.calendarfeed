from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.i18nmessageid import MessageFactory

_ = MessageFactory("collective.calendarfeed")

from .portlet_edit import AddForm,Assignment,ICalendarFeedPortlet,Renderer

#class ICalendarFeedPortlet(IStaticPortlet):
#    """ Defines a new portlet " Calendar Feed" which takes properties of the existing static text portlet. """
#    pass

class CalendarFeedRenderer(Renderer):
    """ Overrides static.pt in the rendering of the portlet. """
    render = ViewPageTemplateFile('portlet_calendar_feed.pt')

class CalendarFeedAssignment(Assignment):
    """ Assigner for google_calendar_feed static portlet. """
    implements(ICalendarFeedPortlet)

class CalendarFeedAddForm(AddForm):
    """ Make sure that add form creates instances of our custom portlet instead of the base class portlet. """
    def create(self, data):
        return CalendarFeedAssignment(**data)
