from django.contrib import admin
from django.urls import path
from django.urls import include

from drf_spectacular.views import SpectacularAPIView,\
                                    SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

from dotenv import load_dotenv
import os
load_dotenv()
ENV = os.environ.get("ENV")

urlpatterns = [
        
    path('admin/',
            admin.site.urls),

    path('api/',
            include(('funnyshopAPI.routers', 'funnyshopAPI')),
            name = 'shop-api'),
    
    path("api/schema/",
            SpectacularAPIView.as_view(),
            name="schema"),

    path("api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view( url_name="schema"),
            name="swagger-ui"),

    path("api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view( url_name="schema"),
            name="swagger-ui"),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)