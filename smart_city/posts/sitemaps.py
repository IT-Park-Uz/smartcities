from django.contrib.sitemaps import Sitemap
from .models import Article, News, Question


class Site:
    domain = 'smartcities.uz'


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    protocol = 'https'

    def get_urls(self, site=None, **kwargs):
        site = Site()
        return super(ArticleSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return Article.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return '/article/%s?lang=gb' % obj.id


class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    protocol = 'https'

    def get_urls(self, site=None, **kwargs):
        site = Site()
        return super(NewsSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return News.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return '/news/%s?lang=gb' % obj.id


class QuestionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def get_urls(self, site=None, **kwargs):
        site = Site()
        return super(QuestionSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return Question.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return '/question/%s?lang=gb' % obj.id
