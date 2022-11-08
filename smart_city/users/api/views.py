from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from config.settings.base import CACHE_TTL
from .permessions import IsOwnerOrReadOnly
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListAPIView, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    # permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filterset_fields = ("username", "first_name", "last_name")
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    # def get_queryset(self, *args, **kwargs):
    #     assert isinstance(self.request.user.id, int)
    #     return self.queryset

    @method_decorator(cache_page(CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        username = request.query_params.get("username")
        if not username:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = self.get_queryset().filter(username=username).first()
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @method_decorator(cache_page(CACHE_TTL))
    @method_decorator(vary_on_cookie)
    @action(detail=False)
    def me(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user, context={"request": request})
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
