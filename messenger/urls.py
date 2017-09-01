from django.conf.urls import url
from messenger.views import WebHookView
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    url(r'^webhook/$', csrf_exempt(WebHookView.as_view())),
]