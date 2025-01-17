from api.views import CommentsViewSet, GroupsViewSet, PostsViewSet
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('posts', PostsViewSet, basename='posts')
router.register('groups', GroupsViewSet, basename='groups')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentsViewSet,
    basename='post-comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
