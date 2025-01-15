from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import CommentsDetail, CommentsList, GroupsViewSet, PostsViewSet

router = DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')
router.register(r'groups', GroupsViewSet, basename='groups')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('api/v1/posts/<int:post_id>/comments/', CommentsList.as_view()),
    path('api/v1/posts/<int:post_id>/comments/<int:pk>/',
         CommentsDetail.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
