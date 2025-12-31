from rest_framework import viewsets 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from api_users.models import User

from .spotify_service import (
    get_token,
    get_artist,
    get_new_releases,
)

# Variable global para almacenar el token
SPOTIFY_ACCESS_TOKEN = None

class SpotifyViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], url_path='token')
    def token(self, request):   
        global SPOTIFY_ACCESS_TOKEN  # Usamos la variable global
        username = request.data.get("username")

        if not username:
             return Response(
                 {"detail": "You must provide a username"},
                 status=status.HTTP_400_BAD_REQUEST
             )

        try:
             user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not registered"},status=status.HTTP_404_NOT_FOUND)

        try:
            token = get_token(
                settings.SPOTIFY_CLIENT_ID,
                settings.SPOTIFY_CLIENT_SECRET,
            )
            # Guardamos el token globalmente
            SPOTIFY_ACCESS_TOKEN = token
        except Exception as e:
            print(f"Error obteniendo el token: {e}")
            return Response(
                {"detail": "Token could not be generated"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response({"access_token": token})

    @action(detail=False, methods=['get'], url_path='artist/(?P<artist_id>[^/.]+)')
    def artist(self, request, artist_id=None):
        global SPOTIFY_ACCESS_TOKEN  # Usamos la variable global

        # Si el token no está disponible, retornamos un error
        if not SPOTIFY_ACCESS_TOKEN:
            return Response(
                {"detail": "Token is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            artist = get_artist(SPOTIFY_ACCESS_TOKEN, artist_id)
        except PermissionError:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except LookupError:
            return Response(
                {"detail": "Artist not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(artist)

    @action(detail=False, methods=['get'], url_path='releases')
    def releases(self, request):
        global SPOTIFY_ACCESS_TOKEN  # Usamos la variable global

        # Si el token no está disponible, retornamos un error
        if not SPOTIFY_ACCESS_TOKEN:
            return Response(
                {"detail": "Token is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            releases = get_new_releases(SPOTIFY_ACCESS_TOKEN)
        except PermissionError:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(releases)
