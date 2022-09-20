from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
# осталось ваши эндпоинты дописать
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"title", TitleViewSet, basename="title")


urlpatterns = [
    path('v1/', include(router.urls)),
    # хз авторизацию так будем делать или еще как-то?
    # path('v1/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
]
