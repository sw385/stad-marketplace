# marketplace/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
	path('', TemplateView.as_view(template_name='index.html'), name='index'),
	path('admin/', admin.site.urls),
	path('users/', include('users.urls')),
	path('users/', include('django.contrib.auth.urls')),
	path('market/', include('market.urls')),
	path('', include('market.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


