from datetime import datetime
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import (
    IsAdmin, IsAdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly
)
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, GetTokenSerializer,
    RegistrationSerializer, ReviewSerializer, TitleDetailSerializer,
    TitleSerializer, UserSerializer
)
from api_yamdb.settings import EMAIL_ADRESS
from reviews.models import Category, Genre, Review, Title, User


class UserViewSet(viewsets.ModelViewSet):
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


class TitleViewSet(viewsets.ModelViewSet):
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
        return self.serializer_class


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_title(self) -> Title:
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_review(self) -> Review:
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    # на основе запроса создаем сериализатор
    serializer = RegistrationSerializer(data=request.data)
    # производим валидацию сериализатора
    serializer.is_valid(raise_exception=True)
    username = request.data["username"]
    email = request.data["email"]
    # проверяем на наличие в базе с таким же именем, но другой почты
    if (User.objects.filter(Q(username=username) & ~Q(email=email)).exists()):
        return Response(
            {'username': 'Пользователь с таким именем уже есть.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # проверяем на наличие в базе с такой же почтой, но другим именем
    if (User.objects.filter(~Q(username=username) & Q(email=email)).exists()):
        return Response(
            {'username': 'Пользователь с такой почтой уже есть.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # получаем либо создаем пользователя
    user, _ = User.objects.get_or_create(**serializer.validated_data)
    # генерируем пин-код (на основе pk и last_login)
    confirmation_code = default_token_generator.make_token(user)
    # отправляем писмо с пин-кодом
    send_mail(
        'Токен',
        f'Ваш токен: {confirmation_code}',
        EMAIL_ADRESS,
        [f'{email}']
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    # на основе запроса создаем сериализатор
    serializer = GetTokenSerializer(data=request.data)
    # производим валидацию сериализатора
    serializer.is_valid(raise_exception=True)
    # получаем из базы пользователя
    user = get_object_or_404(User, username=request.data['username'])
    # проверяем пин-код
    confirmation_code_is_valid = default_token_generator.check_token(
        user, serializer.data['confirmation_code']
    )
    # обновляем last_login, чтобы ранее выданный пин-код перестал быть валидным
    user.last_login = datetime.now()
    user.save()
    if confirmation_code_is_valid:
        return Response(
            {'token': str(RefreshToken.for_user(user).access_token)},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {'confirmation_code': 'Неверный код подверждения.'},
        status=status.HTTP_400_BAD_REQUEST
    )
