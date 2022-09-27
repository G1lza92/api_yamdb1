from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.mixins import PatchModelMixin
from api.permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                             IsAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTokenSerializer,
                             RegistrationSerializer, ReviewSerializer,
                             TitleDetailSerializer, TitleSerializer,
                             UserSerializer)
from api_yamdb.settings import EMAIL_ADRESS
from reviews.models import Category, Genre, Review, Title, User


class ModelWithoutUpdateViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    PatchModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class UserViewSet(ModelWithoutUpdateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False, methods=['get', 'patch'],
        url_name='me', url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def user_information(self, request):
        if request.method == 'GET':
            return Response(
                UserSerializer(request.user).data,
                status=status.HTTP_200_OK
            )
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


class CategoryGenreBaseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    queryset = None
    serializer_class = None
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelWithoutUpdateViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'name', 'description', 'year']
    ordering = ('-rating', 'name', )
    filterset_class = TitleFilter
    serializer_class = TitleSerializer
    detail_serializer_class = TitleDetailSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ReviewViewSet(ModelWithoutUpdateViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_title(self) -> Title:
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(ModelWithoutUpdateViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_review(self) -> Review:
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()


class RegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(delf, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid()
            user = User.objects.get(username=request.data.get('username'))
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Токен',
                f'Ваш токен: {confirmation_code}',
                EMAIL_ADRESS,
                [f'{request.data["email"]}']
            )
            user.is_active = False
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Токен',
                f'Ваш токен: {confirmation_code}',
                EMAIL_ADRESS,
                [f'{request.data["email"]}']
            )
            user = User.objects.get(username=serializer.data.get('username'))
            user.is_active = False
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=request.data['username'])
        confirmation_code = serializer.data.get('confirmation_code')
        if (default_token_generator.check_token(user, confirmation_code)
                and not user.is_active):
            user.is_active = True
            user.save()
            return Response(
                {'token': str(RefreshToken.for_user(user).access_token)},
                status=status.HTTP_201_CREATED
            )
        return Response(
               {confirmation_code: 'Неверный код подверждения'},
               status=status.HTTP_400_BAD_REQUEST
            )
