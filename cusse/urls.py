from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^docs/', include('rest_framework_docs.urls')),

    url(r'^blog/', include('blog.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^events/', include('events.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# local
# wsgi dev server(serve static/media)

# stage/dev/prod
# web-server(nginx, apache), server static/media