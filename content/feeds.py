from django.contrib.syndication.feeds import Feed
from models import *
from crimsononline.common.templatetags.common import human_list
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from crimsononline.settings import URL_BASE, CACHE_STANDARD, CACHE_LONG

TITLE_BASE = "The Harvard Crimson" + " | "
NUM_STORIES = 25

class CrimsonFeed(Feed):
    def item_author_name(self, item):
        return human_list(item.contributors.all())
    
    def item_author_link(self, item):
        if(item.contributors.all().count() == 1):
            return URL_BASE + item.contributors.all()[0].get_absolute_url()
            
    title_template = 'feeds/title.html'
    description_template = 'feeds/description.html'

class Latest(CrimsonFeed):
    title = TITLE_BASE + "All Articles"
    link = "/"
    description = "The latest Crimson articles"

    # 6 is Flyby. No idea if this will help
    
    def items(self):
        latestitems = cache.get('feeds_latest')
        if not latestitems:
            latestitems = Article.objects.exclude(section=6).order_by('-issue__issue_date')[:NUM_STORIES]
            cache.set('feeds_latest', latestitems, CACHE_STANDARD)
        return Article.objects.exclude(section=6).order_by('-issue__issue_date')[:NUM_STORIES]

class TopNews(CrimsonFeed):
    title = TITLE_BASE + "Top Stories"
    link = "/"
    description = "The top Crimson articles"

    # 6 is Flyby. No idea if this will help

    def items(self):
        topitems = cache.get('feeds_top')
        if not topitems:
            topitems = Article.objects.exclude(section=6).order_by('-issue__issue_date').exclude(priority__lte=5)[:NUM_STORIES]
            cache.set('feeds_top', topitems, CACHE_STANDARD)
        return topitems
    

class ByAuthor(CrimsonFeed):

    def get_object(self, bits):
        # Should be feeds/author/[id], not feeds/author/[id]/bullshit
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Contributor.objects.get(pk=bits[0])
    
    def title(self, obj):
        return TITLE_BASE + "Articles by %s" % unicode(obj)
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()
    
    def description(self, obj):
        return "The latest Crimson articles by %s" % str.capitalize(str(obj))

    def items(self, obj):
        items = cache.get('feeds_author_%d' % obj.pk)
        if not items:
            items = Article.objects.filter(contributors__id__exact=obj.pk).order_by('-issue__issue_date')[:NUM_STORIES]
            cache.set(('feeds_author_%d' % obj.pk), items, CACHE_LONG)
        return items
    

class ByTag(CrimsonFeed):
    # Should be feeds/tag/ninja_stuff to access tag Ninja Stuff
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(text__iexact=bits[0].replace('_', ' '))
    
    def title(self, obj):
        return TITLE_BASE + "Tag: %s" % unicode(obj)
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        
        return obj.get_absolute_url()
    
    def description(self, obj):
        return "The latest Crimson articles tagged with %s" % str.capitalize(str(obj))
    
    def items(self, obj):
        items = cache.get('feeds_tag_%d' % obj.pk)
        if not items:
            items = Article.objects.filter(tags__id__exact=obj.pk).order_by('-issue__issue_date')[:NUM_STORIES]
            cache.set('feeds_tag_%d' % obj.pk, items, CACHE_LONG)
        return items
    

class BySection(CrimsonFeed):
    # Should be feeds/section/arts
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Section.objects.get(name__iexact=bits[0].replace('_', ' '))
    
    def title(self, obj):
        return TITLE_BASE + "%s" % unicode(obj)
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        if hasattr(obj,'get_absolute_url'):
            return obj.get_absolute_url()
        else:
            return 
    
    def description(self, obj):
        return "The latest Crimson articles in %s" % str.capitalize(str(obj))
    
    def items(self, obj):
        items = cache.get('feeds_section_%d' % obj.pk)
        if not items:
            items = Article.objects.filter(section__exact=obj.pk).order_by('-issue__issue_date')[:NUM_STORIES]
            cache.set('feeds_section_%d' % obj.pk, items, CACHE_STANDARD)
        return items
    
