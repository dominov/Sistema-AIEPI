from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout, password_change, password_change_done


# my urls
from django.views.generic.base import TemplateView

from poll.views import views
from siaiepi.views import login

urlpatterns = [
    url(r'^$', views.DemographicsFormView.as_view(), name='home'),
    url(r'^poll/', include('poll.urls', namespace='poll', app_name='poll')),
]

# django urls
urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, {'template_name': 'pages/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url('^password_change/', password_change, {'template_name': 'registration/password_change.html'},
        name='password_change'),
    url('^password_change_done/', password_change_done, {'template_name': 'pages/password_change_done.html'},
        name='password_change_done'),
]

# fiber url
# urlpatterns += [
#     url(r'^admin/fiber/', include('fiber.admin_urls')),
#     url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('fiber',),}),
#     url(r'^api/v2/', include('fiber.rest_api.urls')),
#     url(r'', 'fiber.views.page'),
# ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
