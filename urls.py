from os import path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import *
from crimsononline.admin_cust.views import login_user
from django.contrib.auth.views import login, logout
from django.contrib.sitemaps import FlatPageSitemap
from django.views.generic.simple import redirect_to
from crimsononline.content.sitemaps import ArticleSitemap

FILTER_URL_RE = r'(page/(?P<page>\d+)/)?(sections/(?P<sections>[\w,]+)/)?' \
    '(types/(?P<types>[\w,]+)/)?'

from crimsononline.content import feeds

urlpatterns = patterns('',
)

urlpatterns += patterns('crimsononline.content.views',
    url(r'writer/(?P<pk>\d+)/(?P<f_name>[\w\-\'\.\s]+)_' \
        r'(?P<m_name>[\w\-\'\.\s]*)_(?P<l_name>[\w\-\'\.\s]+)/%s$' % FILTER_URL_RE,
        'writer', name='content_writer_profile'),
    url(r'^section/', include('crimsononline.content.section_urls'), name='content_section'),
    url(r'^tag/(?P<tag>[\w&\'\s-]+)/%s$' % FILTER_URL_RE, 
        'tag', name='content_tag'),
    url(r'^$', 'index', name='content_index'),
    url(r'^issue/(\d+)/(\d+)/(\d+)/$', 'index', name='content_index'),    
    url(r'^subscribe/', include('crimsononline.subscriptions.urls')),
    url(r'^about/', include('crimsononline.info.urls')),
    url(r'^iphone/(?P<s>\w+)/$', 'iphone'),
    url(r'^classifieds/$',redirect_to, {'url':'http://ad2ad.com/?portalid=1708065'}),
)

urlpatterns += patterns('',
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
)

feeds = {
    'latest': feeds.Latest,
    'section': feeds.BySection,
    'author': feeds.ByAuthor,
    'tag': feeds.ByTag,
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'articles': ArticleSitemap,
}

urlpatterns +=patterns('',
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^sitemap/$', 'crimsononline.content.views.sitemap'),
    url(r'^sitemap/(\d{4})/$', 'crimsononline.content.views.sitemap'),
    url(r'^sitemap/(\d{4})/(\d+)/$', 'crimsononline.content.views.sitemap'),
)

"""
urlpatterns += patterns('django.views.generic.simple',
    (r'login/$', 'redirect_to', { 'url': 'http://www.alondite.com/welp/crimlogin.html'}),
    (r'login_return/$', login_user),
)
"""

admin.autodiscover()

urlpatterns += patterns('',
    (r'^admin/', include('crimsononline.admin_cust.urls')),
)

# generic content urls
CONTENT_URL_RE = r'([\w\-]+)/(\d{4})/(\d{1,2})/(\d{1,2})/([0-9\w_\-%]+)/$'
CGROUP_URL_RE = r'([\w]+)/([\w0-9\-]+)/'
generic_patterns = patterns('crimsononline.content.views',
    url('^' + CONTENT_URL_RE, 'get_content', name='content_content'),
    url('^' + CGROUP_URL_RE + CONTENT_URL_RE, 'get_grouped_content',
        name='content_grouped_content'),
    url('^' + CGROUP_URL_RE + '$', 'get_content_group', 
        name='content_contentgroup'),
)
urlpatterns += generic_patterns

if settings.HAYSTACK:
    import haystack
    haystack.autodiscover()
    
    from crimsononline.search.forms import DateRangeSearchForm
    from crimsononline.search.views import AjaxSearchView
    
    urlpatterns += patterns('search.views',
        url(r'^search/', AjaxSearchView(form_class=DateRangeSearchForm)))

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT}),    
    )

urlpatterns += patterns('',
    (r'', include('crimsononline.legacy.urls')),
)
