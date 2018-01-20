from django.conf.urls import include, url
from django.contrib import admin
from chatterbot.ext.django_chatterbot import urls as chatterbot_urls
# from example_app.views import ChatterBotAppView

from example_app import views as vs

urlpatterns = [
    # url(r'^$', ChatterBotAppView.as_view(), name='main'),
    url(r'^$', vs.displayAnswer, name='main'),
    url(r'^chat/', vs.json_page, name='chat'),
    url(r'^chat_state/', vs.chat_state, name='chat_state'),
    url(r'^reset_chat/', vs.reset_chat, name='reset_chat'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    # url(r'^api/chatterbot/', include(chatterbot_urls, namespace='chatterbot')),
]
