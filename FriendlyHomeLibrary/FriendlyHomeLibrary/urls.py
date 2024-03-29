"""FriendlyHomeLibrary URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from FHLBuilder import urls as builder_urls
from FHLBuilder import views as bv

from FHLReader import urls as reader_urls

from FHLUser import urls as user_urls

urlpatterns = [
    url(r'^$',bv.HomePage.as_view(),name='homepage'),
    url(r'^admin/', admin.site.urls),
    url(r'^builder/',include(builder_urls)),
    url(r'^reader/',include(reader_urls)),
    url(r'^user/',include(user_urls)),    
]
'''
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__DEBUG__/',include(debug_toolbar.urls)),
    ] + urlpatterns
'''

