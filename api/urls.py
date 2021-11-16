from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    RegistrationAPIView, ReviewViewSet, TitleViewSet,
                    TokenAPIView, UserViewSet)

router = DefaultRouter()

router.register(
    'users',
    UserViewSet, basename='users'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

router.register(
    'titles',
    TitleViewSet, basename='posts'
)
router.register(
    'genres',
    GenreViewSet, basename='posts'
)
router.register(
    'categories',
    CategoryViewSet, basename='posts'
)

app_name = 'api'
urlpatterns = [
    path('v1/auth/email/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', TokenAPIView.as_view()),
    path('v1/', include(router.urls)),
]
