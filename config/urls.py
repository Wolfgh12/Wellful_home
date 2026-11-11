from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from catalog import views as catalog_views

# Supreme Admin Dashboard Customization
admin.site.site_header = "Wellful Home Administration"
admin.site.site_title = "Wellful Home Admin Portal"
admin.site.index_title = "Wellful Home Management Dashboard"

urlpatterns = [
    # PWA Service Worker & Web Manifest served at root scope
    path('sw.js', TemplateView.as_view(
        template_name='sw.js',
        content_type='application/javascript'
    ), name='service_worker'),
    path('manifest.json', TemplateView.as_view(
        template_name='manifest.json',
        content_type='application/manifest+json'
    ), name='web_manifest'),
    
    path('admin/', admin.site.urls),
    path('', catalog_views.home, name='home'),
    path('catalog/', include('catalog.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)