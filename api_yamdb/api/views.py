from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated

from reviews.models import Categories, Genres, Title

