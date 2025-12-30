import requests
import base64


SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"


import requests
import base64


SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"


def get_token(client_id: str, client_secret: str) -> str:
    basic_auth = f"{client_id}:{client_secret}"
    encoded = base64.b64encode(basic_auth.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)

    # Imprimir detalles de la respuesta para depuración
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")

    if response.status_code != 200:
        raise Exception(f"Token could not be generated, status code: {response.status_code}, response: {response.text}")

    return response.json()["access_token"]

def get_artist(token: str, artist_id: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{SPOTIFY_API_BASE}/artists/{artist_id}", headers=headers
    )

    if response.status_code == 401:
        raise PermissionError("Invalid token")

    if response.status_code != 200:
        raise LookupError("Artist not found")

    return response.json()


def get_new_releases(token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{SPOTIFY_API_BASE}/browse/new-releases", headers=headers
    )

    if response.status_code == 401:
        raise PermissionError("Invalid token")

    if response.status_code != 200:
        raise Exception("Could not fetch new releases")

    return response.json()


def get_artist(token: str, artist_id: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{SPOTIFY_API_BASE}/artists/{artist_id}", headers=headers
    )

    if response.status_code == 401:
        raise PermissionError("Invalid token")

    if response.status_code != 200:
        raise LookupError("Artist not found")

    return response.json()


def get_new_releases(token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{SPOTIFY_API_BASE}/browse/new-releases", headers=headers
    )

    if response.status_code == 401:
        raise PermissionError("Invalid token")

    if response.status_code != 200:
        raise Exception("Could not fetch new releases")

    return response.json()
