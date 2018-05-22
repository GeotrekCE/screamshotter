from django.conf.urls import include, url
from screamshotter.views import view as headless

urlpatterns = [
    url(r'headless/', headless, name='headless'),
    url(r'',  include('screamshot.urls', namespace='screamshot', app_name='screamshot')),
]
