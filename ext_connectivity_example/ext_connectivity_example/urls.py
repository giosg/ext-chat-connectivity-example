from django.urls import include, path
from django.views.generic.base import RedirectView

from giosg_webhooks import urls as giosg_webhook_urls
from chat_app import urls as chat_app_urls

urlpatterns = [
    path('', include(giosg_webhook_urls.urlpatterns)),
    path('', include(chat_app_urls.urlpatterns)),
    path('', RedirectView.as_view(url='/chat-app/')),

]
