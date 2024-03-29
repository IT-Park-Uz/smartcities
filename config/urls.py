from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from smart_city.posts.sitemaps import ArticleSitemap, NewsSitemap, QuestionSitemap

from smart_city import social_auth

sitemaps = {
    "question": QuestionSitemap,
    "news": NewsSitemap,
    "article": ArticleSitemap
}

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/main_menu.html"), name="home"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("accounts/", include("allauth.urls")),
    path("ckeditor/", include('ckeditor_uploader.urls')),
    path("users/", include("smart_city.users.urls", namespace="users")),
    path("itpark/", include("smart_city.itpark.urls", namespace="itpark")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("v1/", include("config.api_router")),
    # DRF auth token
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        settings.API_DOCS_URL,
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

admin.site.site_header = "Модерация - Smart City"
admin.site.index_title = "Добро пожаловать в модерацию"
admin.site.site_title = "Туториал модерации"
admin.site.index_template = 'admin/index.html'
admin.autodiscover()
