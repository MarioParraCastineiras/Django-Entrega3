from rest_framework import viewsets 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    @action(detail=False, methods=['get'], url_path='by-name/(?P<username>[^/.]+)')
    def get_by_username(self, request, username=None):
        try:
            user = User.objects.get(username=username)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail":"User not fund"}, status=status.HTTP_404_NOT_FOUND)
