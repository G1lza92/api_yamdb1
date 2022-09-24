from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdminOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTokenSerializer,
                             RegistrationSerializer, ReviewSerializer,
                             TitleSerializer, UserSerializer)
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score'))


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.get_post().reviews

    def get_post(self) -> Title:
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RegistrationViewSet(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get('username') == 'me':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        response = super().create(request, *args, **kwargs)
        headers = self.get_success_headers(response.data)
        return Response(
            response.data, status=status.HTTP_200_OK, headers=headers
        )

    def perform_create(self, serializer):
        confirmation_code = '2222'  # здесь нужно генерить нормальный код
        send_mail(
            'Токен',
            f'Ваш токен: {confirmation_code}',
            'yamdb@yandex.ru',
            [f'{self.request.data["email"]}']
        )
        serializer.save(confirmation_code=confirmation_code)


class GetTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid()
        data = serializer.validated_data
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response(
                {data.get('username'): 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.data.get('confirmation_code') == user.confirmation_code:
            return Response(
                {'token': str(RefreshToken.for_user(user).access_token)},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {data.get('confirmation_code'): 'Неверный код подверждения'},
            status=status.HTTP_404_NOT_FOUND
        )
