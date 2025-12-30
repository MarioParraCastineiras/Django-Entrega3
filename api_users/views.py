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



# @app.post("/spotify/token")
# async def spotifytoken(request: Request):
#     global SPOTIFY_TOKEN_GLOBAL
    
#     data = await request.json()
#     username = data.get("username")

#     if not username:
#         raise HTTPException(status_code=400, detail="You must provide a username")

#     mydb = DataBaseConnection(host="localhost", user="root", password="123123123", database="ENTREGA1")
#     mydb_conn = mydb.get_connection()
#     mycursor = mydb_conn.cursor()

#     mycursor.execute("SELECT * FROM users WHERE username=%s", (username,))
#     user = mycursor.fetchone()
#     mydb_conn.commit()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not registered. Please register to get access")
    
#     SPOTIFY_TOKEN_GLOBAL = get_Token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
#     if "error" in SPOTIFY_TOKEN_GLOBAL:
#         raise HTTPException(status_code=404, detail="Token couldn't be generated")
#     return JSONResponse(content=SPOTIFY_TOKEN_GLOBAL, status_code=200)
#     print(SPOTIFY_TOKEN_GLOBAL)

# @app.get("/spotify/artist/{id}")
# async def artistinfo(id: str):
#     global SPOTIFY_TOKEN_GLOBAL
#     artist_data=get_Artists(SPOTIFY_TOKEN_GLOBAL, id)
#     if "error" in artist_data:
#         raise HTTPException(status_code=404, detail="Artist Not found")
#     if "token_error" in artist_data:
#         raise HTTPException(status_code=401, detail="Invalid token. Please try again with a new token")
#     return JSONResponse(content=artist_data, status_code=200)
#     print(artist_data)

# @app.get("/spotify/releases")
# async def newreleases():
#     global SPOTIFY_TOKEN_GLOBAL
#     releases_data = get_NewReleases(SPOTIFY_TOKEN_GLOBAL)

#     if "error" in releases_data:
#         raise HTTPException(status_code=404, detail="Unable to load latest data, try again later")
#     if "token_error" in releases_data:
#         raise HTTPException(status_code=401, detail="Invalid token. Please try again with a new token")
#     return JSONResponse(content=releases_data, status_code=200)
#     print(releases_data)