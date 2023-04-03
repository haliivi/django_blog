from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.urls import path, include

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('blog/<slug>/', PostDetailView.as_view(), name='post_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
