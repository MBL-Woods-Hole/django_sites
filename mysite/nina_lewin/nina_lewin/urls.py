"""nina_lewin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^nina_lewin_website/', include('nina_lewin_website.urls')),
    url(r'^admin/', admin.site.urls),
    # url(r'^metadata_template/', include('metadata_template.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
# ]
#
# urlpatterns += [
#     path('nina_lewin/', include('nina_lewin.urls')),
# ]
#
# urlpatterns += [
#     path('', RedirectView.as_view(url='/nina_lewin/', permanent=True)),
# ]
#
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
