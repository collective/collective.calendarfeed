import re
import requests
import logging

from datetime import date
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.app.portlets.portlets import base
from zope import schema
from zope.interface import implements
from zope.component.interfaces import ComponentLookupError
from zope.component import getUtility
from zope.formlib import form

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.i18nmessageid import MessageFactory

_ = MessageFactory("collective.calendarfeed")

from zope.component import getUtility
from zope.security import checkPermission
from plone.registry.interfaces import IRegistry

logger = logging.getLogger('collective.calendarfeed')

try:
    registry = getUtility(IRegistry)
except ComponentLookupError:
    registry = {
        'collective.calendarfeed.settings.ISettings.google_apikey':
          u"",
        'collective.calendarfeed.settings.ISettings.calendar_address':
          u""
        }
        
calendarfeed_settings = {
    "google_apikey":
    registry['collective.calendarfeed.settings.ISettings.google_apikey'],
    "calendar_address":
   registry['collective.calendarfeed.settings.ISettings.calendar_address']
                    }


class ICalendarFeedPortlet(IPortletDataProvider):
    """A portlet which renders a google calendar feeed
    
    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    google_apikey = schema.TextLine(
        title=_(u" Calendar API key"),
        description=_(u"Calendar API key from google"),
        default = calendarfeed_settings['google_apikey'],
        required=True)
    calendar_address = schema.TextLine(
        title=_(u"Calendar Address"),
        description=_(u"Address of the google calendar feed usually in the form 'user-calendar@gmail.com'"),
        default = calendarfeed_settings['calendar_address'],
        required=False)
    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        constraint=re.compile("[^\s]").match,
        required=False)

    text = schema.Text(
        title=_(u"Content before feed (optional)"),
        description=_(u"Content added here will go before the calendar feed"),
        required=False)
    
    maxitems = schema.Int(
        title=_(u"Maximum Items"),
        description=_(u"Number of items to show. Leave blank to show all"
            ),
        required=False,
        default=4)

    footer = schema.TextLine(
        title=_(u"Portlet footer"),
        description=_(u"Text to be shown in the footer," 
                      " you could use this to link to the calendar page"),
        required=False)

    more_url = schema.ASCIILine(
        title=_(u"Details link"),
        description=_(u"If given, the header and footer "
            "will link to this URL."),
        required=False)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ICalendarFeedPortlet)

    header = _(u"title_google_calendar_feed_portlet", default=u" Calendar Feed portlet")
    text = u""
    footer = u""
    more_url = ''

    def __init__(self, header=u"", text=u"", calendar_address=u"",
                   google_apikey=u"", maxitems=4, footer=u"",
                   more_url=''):
        self.header = header
        self.text = text
        self.footer = footer
        self.more_url = more_url
        self.maxitems = maxitems
        self.calendar_address = calendar_address
        self.google_apikey = google_apikey

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave or
        static string if title not defined.
        """
        return self.header or _(u'portlet_calendar_feed', default=u" Calendar Feed Portlet")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('portlet_calendar_feed.pt')

    def css_class(self):
        """Generate a CSS class from the portlet header
        """
        header = self.data.header
        if header:
            normalizer = getUtility(IIDNormalizer)
            return "portlet-calendar-feed-%s" % normalizer.normalize(header)
        return "portlet-calendar-feed"

    def has_link(self):
        return bool(self.data.more_url)

    def has_footer(self):
        return bool(self.data.footer)
    
    @property
    def js(self):
    
        params = {
          "apikey": self.data.google_apikey,
          "baseurl": "https://www.googleapis.com/calendar/v3/calendars",
          "calendarid" : self.data.calendar_address,
          "css_class" : self.css_class(),
          "max"     : self.data.maxitems,
          "now" : u"%sT00:00:00Z" % unicode(date.today().isoformat())
          }
         
        url =  "%(baseurl)s/%(calendarid)s/events?singleEvents=true&timeMin=%(now)s&maxResults=%(max)s&orderBy=startTime&key=%(apikey)s" % params
        js_script = """<script type="text/javascript">
$(document).ready(function() {
var url =  "%(baseurl)s/%(calendarid)s/events?singleEvents=true&timeMin=%(now)s&maxResults=%(max)s&orderBy=startTime&key=%(apikey)s";
$.getJSON(url, function(data) {
    for(i in data['items']) {
        item = data['items'][i];
        var date = '';
        if ('dateTime' in item.start) {
           date = item.start.dateTime.split("T")[0]
        }  
        if ('date' in item.start) {
           date = item.start.date;
        } 
        date = moment(date, "YYYY-MM-DD").format('MMMM Do YYYY')
        $(".portlet.%(css_class)s").append(
        "<dd class='portletItem google-feed-event'>" 
        + "<a class='item-event' href='" + item.htmlLink + "'>" + item.summary + "</a>" 
        + "<br />"
        + "<span class='item-date'>" + date + "</span><br />" 
        + "</dd>"
        );
    }
});
});
</script>
"""
        return {
          "script":js_script % params,
          "url":url
         }       
      
    def json_feed(self):
        params = {
          "baseurl": "https://www.googleapis.com/calendar/v3/calendars",
          "calendarid" : self.data.calendar_address,
          "apikey": self.data.google_apikey
          }
        target = "%(baseurl)s/%(calendarid)s/events" % params
        payload = {'key': params['apikey']}
        r = requests.get(target, params=payload)
        return r.json()

    def transformed(self, mt='text/x-html-safe'):
        """Use the safe_html transform to protect text output. This also
        ensures that resolve UID links are transformed into real links.
        """
        orig = self.data.text
        context = aq_inner(self.context)
        if not isinstance(orig, unicode):
            # Apply a potentially lossy transformation, and hope we stored
            # utf-8 text. There were bugs in earlier versions of this portlet
            # which stored text directly as sent by the browser, which could
            # be any encoding in the world.
            orig = unicode(orig, 'utf-8', 'ignore')
            logger.warn(" Calendar Feed portlet at %s has stored non-unicode text. "
                "Assuming utf-8 encoding." % context.absolute_url())

        # Portal transforms needs encoded strings
        orig = orig.encode('utf-8')

        transformer = getToolByName(context, 'portal_transforms')
        data = transformer.convertTo(mt, orig,
                                     context=context, mimetype='text/html')
        result = data.getData()
        if result:
            if isinstance(result, str):
                return unicode(result, 'utf-8')
            return result
        return None


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ICalendarFeedPortlet)
    form_fields['text'].custom_widget = WYSIWYGWidget
    label = _(u"title_add_calendar_feed_portlet", default=u"Add Calendar Feed portlet")
    description = _(u"Calendar Feed Portlet",
        default=u"A portlet which displays a Calendar feed.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ICalendarFeedPortlet)
    form_fields['text'].custom_widget = WYSIWYGWidget
    label = _(u"title_edit_calendar_feed_portlet", default=u"Edit google calendar feed portlet")
    description = _(u"description_calendar_feed_portlet",
        default=u"A portlet which can display google calendar feed HTML text.")
