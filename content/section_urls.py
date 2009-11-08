from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('crimsononline.content.views',
    url(r'^news/$', 'section_news', name='content.section.news'),
    url(r'^sports/$', 'section_sports', name='content.section.sports'),
    url(r'^photo/$', 'section_photo', name='content.section.photo'),
    url(r'^opinion/$', 'section_opinion', name='content.section.opinion'),
    url(r'^flyby/$', 'section_flyby', name='content.section.flyby'),
    url(r'^fm/$', 'section_fm', name='content.section.fm'),
    url(r'^fml/$', redirect_to, {'url': 'http://fmylife.com'}),
    url(r'^arts/$', 'section_arts', name='content.section.arts'),
)
