import random
import string

import django_filters.rest_framework
from django.db.models import Avg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Review, Comment, Title, Genre, Category
from .permissions import (IsAdminPermission,
                          IsAdminOrReadOnlyPermission, IsAuthorOrStaffReadOnly)
from .serializers import (RegistrationSerializer, TokenSerializer,
                          UserSerializer, TitleWriteSerializer,
                          TitleReadSerializer, GenreSerializer,
                          CategorySerializer, ReviewSerializer,
                          CommentSerializer)
from .filters import TitleFilter
from .custom_views import CreateListDestroyViewSet
from .custom_pagination import CustomPaginationClass


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conf_code = "".join(random.choices(string.ascii_uppercase
                                           + string.digits, k=6))
        send_mail("Your confirmation code for YaMDB",
                  f"Here is the code: {conf_code}",
                  "from@example.com",
                  [request.data["email"]],
                  fail_silently=False, )
        serializer.save(password=conf_code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)
    pagination_class = CustomPaginationClass
    lookup_field = "username"

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['get', 'patch'], url_path='me', )
    def update_self(self, request):
        # user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(request.user, data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrStaffReadOnly, ]
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrStaffReadOnly, ]
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.annotate(rating=Avg('reviews__score')).order_by('-id')
    )
    permission_classes = [IsAdminOrReadOnlyPermission, ]
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    ]
    search_fields = ["title", ]
    filterset_class = TitleFilter
    pagination_class = CustomPaginationClass

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleReadSerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnlyPermission, ]
    filter_backends = [
        filters.SearchFilter
    ]
    lookup_field = 'slug'
    search_fields = ["name", ]
    pagination_class = CustomPaginationClass


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnlyPermission, ]
    filter_backends = [
        filters.SearchFilter
    ]
    lookup_field = 'slug'
    search_fields = ["name", ]
    pagination_class = CustomPaginationClass
