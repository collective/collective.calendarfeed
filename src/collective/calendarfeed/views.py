from Products.Five import BrowserView
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("collective.calendarfeed")

from zope.component import getUtility
from zope.security import checkPermission
from plone.registry.interfaces import IRegistry


class CalendarView(BrowserView):
    """@@calendar view"""
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def canManageSite(self):
        return checkPermission('cmf.ManagePortal', self.context)
      
    def js(self):
        registry = getUtility(IRegistry)
        return """<script>
 $(document).ready(function() {
  $('#calendar').fullCalendar({
                        header: {
     left: 'prev,next today',
     center: 'title',
     right: 'month,agendaWeek,agendaDay'
    },
      //defaultDate: '2014-11-12',
     googleCalendarApiKey: '%(google_apikey)s',
      events: '%(calendar_address)s',
     eventClick: function(event) {
     // opens events in a popup window
     window.open(event.url, 'gcalevent', 'width=700,height=600');
      return false;
   },
   loading: function(bool) {
    $('#loading').toggle(bool);
  }
 });
 });
</script>""" % {
   "google_apikey":
   registry['collective.calendarfeed.settings.ISettings.google_apikey'],
   "calendar_address":
   registry['collective.calendarfeed.settings.ISettings.calendar_address']
                    }

#        return super(CalendarView, self).__call__()
    
