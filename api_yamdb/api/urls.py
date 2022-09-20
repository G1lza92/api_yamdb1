from django.urls import include, path

from api.views import CategoriesViewSet, GenresViewSet, TitleViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"categories", CategoriesViewSet, basename="categories")
router.register(r"genres", GenresViewSet, basename="genres")
router.register(r"title", TitleViewSet, basename="title")


urlpatterns = [
    path('v1/', include(router.urls)),
    # хз авторизацию так будем делать или еще как-то?
    # path('v1/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
]