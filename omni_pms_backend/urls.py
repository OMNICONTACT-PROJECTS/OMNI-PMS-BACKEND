from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions, authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="OMNICONTACT PMS BACKEND API",
        default_version="v1",
        description="OMNICONTACT PMS BACKEND API",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
    authentication_classes=[],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/v1/organisations/", include("organisations.urls")),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/users/", include("accounts.users.urls")),
    path("api/v1/user_documents/", include("accounts.user_docs.urls")),
    path(
        "api/v1/educational_qualification/",
        include("accounts.educational_qualifications.urls"),
    ),
    path("api/v1/devs/", include("devs.urls")),
    path("api/v1/superusers/", include("superusers.urls")),
    path("api/v1/administrators/", include("administrators.urls")),
    path("api/v1/subscribers/", include("subscribers.urls")),
    path("api/v1/departments/", include("departments.urls")),
    path(
        "api/v1/inbound/voice-insights/",
        include("inbound_insights.voice_insights.urls"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
