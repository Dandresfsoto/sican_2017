from django.conf.urls import url
from inbox.views import Inbox

urlpatterns = [
    url(r'$', Inbox.as_view()),
]