from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from .views import *
from django.urls import path, include

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('blog/<slug>/', PostDetailView.as_view(), name='post_detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout',),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
