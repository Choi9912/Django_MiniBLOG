from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),  # allauth URL
    path("blog/", include("blog.urls")),  # 블로그 앱의 URL
    path(
        "", RedirectView.as_view(url="/blog/", permanent=True)
    ),  # 루트 URL을 블로그로 리다이렉트
    path("summernote/", include("django_summernote.urls")),
]

# 정적 파일 및 미디어 파일 서빙을 위한 설정 (개발 환경에서만 사용)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
