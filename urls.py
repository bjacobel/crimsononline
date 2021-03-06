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
    #url(r'^feeds/', 'feedsDown', name='feeds_down'), #put in until RSS feed functionality can be rewritten
    url(r'^issue/(\d+)/(\d+)/(\d+)/$', 'index', name='content_index'),
    url(r'^subscribe/', include('crimsononline.subscriptions.urls')),
    url(r'^contact/', 'contact'),
    url(r'^iphone/(?P<s>\w+)/$', 'iphone'),
    url(r'^classifieds/$',redirect_to, {'url':'http://ad2ad.com/?portalid=1708065'}),
    url(r'^donate/$', redirect_to, {'url': '/about/donate/'}),
    url(r'^feature/(?P<title>[0-9\w_\-%]+)/(?P<sectionTitle>[0-9\w_\-%]+)/(?P<mediaSlug>[0-9\w_\-%]+)/$', 'feature_view', name='feature_package'),
    url(r'^feature/(?P<title>[0-9\w_\-%]+)/(?P<sectionTitle>[0-9\w_\-%]+)/$', 'feature_view', name='feature_package'),
    url(r'^feature/(?P<title>[0-9\w_\-%]+)/$', 'feature_view', name='feature_package'),
)

urlpatterns += patterns('',
    (r'^feeds/top/$', 'django.views.static.serve',
        {'path': '/feeds/TopNews.xml',
         'document_root': settings.MEDIA_ROOT}),
    (r'^feeds/latest/$', 'django.views.static.serve',
        {'path': '/feeds/LatestNews.xml',
         'document_root': settings.MEDIA_ROOT}),
    (r'^feeds/section/arts/$', 'django.views.static.serve',
        {'path': '/feeds/arts.xml',
         'document_root': settings.MEDIA_ROOT}),
    (r'^feeds/section/fm/$', 'django.views.static.serve',
        {'path': '/feeds/fm.xml',
         'document_root': settings.MEDIA_ROOT}),
    (r'^feeds/section/news/$', 'django.views.static.serve',
        {'path': '/feeds/news.xml',
         'document_root': settings.MEDIA_ROOT}),
    (r'^feeds/section/sports/$', 'django.views.static.serve',
        {'path': '/feeds/sports.xml',
         'document_root': settings.MEDIA_ROOT}),
    (r'^feeds/section/flyby/$', 'django.views.static.serve',
        {'path': '/feeds/flyby.xml',
         'document_root': settings.MEDIA_ROOT}),
    (r'^feeds/section/opinion/$', 'django.views.static.serve',
        {'path': '/feeds/opinion.xml',
         'document_root': settings.MEDIA_ROOT})
)

urlpatterns += patterns('',
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
)

feeds = {
    #'latest': feeds.Latest,
    #'top': feeds.TopNews,
    #'section': feeds.BySection,
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
    url(r'^sitemap/contributors/$', 'crimsononline.content.views.sitemap_contributors'),
    url(r'^sitemap/contributors/page/(\d+)/$', 'crimsononline.content.views.sitemap_contributors'),
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
# special stuff

urlpatterns += patterns('crimsononline.content.views',
    url(r'^commencement2010/$', 'commencement2010'),
    url(r'^commencement2010/1960/$', 'commencement2010_1960'),
    url(r'^commencement2010/1985/$', 'commencement2010_1985'),
    url(r'^commencement2010/yir/$', 'commencement2010_yir'),
    url(r'^commencement2010/sports/$', 'commencement2010_sports'),
    url(r'^commencement2010/seniors/$', 'commencement2010_seniors'),
    url(r'^commencement2010/pov/$', 'commencement2010_pov'),
)

admin.autodiscover()

urlpatterns += patterns('',
    (r'^admin/', include('crimsononline.admin_cust.urls')),
)

# generic content urls
CONTENT_URL_RE = r'(?P<ctype>[\w\-]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/' \
                  '(?P<day>\d{1,2})/(?P<slug>[0-9\w_\-%]+)/$'
CGROUP_URL_RE = r'(?P<gtype>[\w]+)/(?P<gname>[\w0-9\-]+)/'
CGROUP_FILTER_URL_RE = r'(page/(?P<page>\d+)/)?(tags/(?P<tags>[,\w&\'\s-]+)/)?'

generic_patterns = patterns('crimsononline.content.views',
    url('^' + CONTENT_URL_RE, 'get_content', name='content_content'),
    url('^' + CGROUP_URL_RE + CONTENT_URL_RE, 'get_grouped_content',
        name='content_grouped_content'),
    url('^' + CGROUP_URL_RE + CGROUP_FILTER_URL_RE + '$', 'get_content_group',
        name='content_contentgroup'),
)
urlpatterns += generic_patterns

"""
if settings.HAYSTACK:
    import haystack
    haystack.autodiscover()

    from crimsononline.search.forms import DateRangeSearchForm
    from crimsononline.search.views import AjaxSearchView

    
"""
urlpatterns += patterns('crimsononline.search.views',
        url(r'^search/', 'searchView'))

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns('',
    (r'^robots\.txt$', 'django.views.static.serve',
        {'path': '/txt/robots.txt',
         'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += patterns('',
    (r'', include('crimsononline.legacy.urls')),
)
