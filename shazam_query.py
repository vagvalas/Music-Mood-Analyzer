import re
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

COUNTRY = "GR"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("&", " and ")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"\[[^\]]*\]", " ", text)
    text = re.sub(r"\b(feat|ft)\.?\b.*", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def search_shazam_song(term: str, country: str = COUNTRY, limit: int = 3) -> dict:
    url = f"https://www.shazam.com/services/amapi/v1/catalog/{country}/search"
    params = {
        "types": "songs",
        "term": term,
        "limit": limit
    }

    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def score_candidate(spotify_track: dict, candidate: dict) -> float:
    score = 0.0

    spotify_title = normalize(spotify_track.get("track_name", ""))
    spotify_artist = normalize(spotify_track.get("main_artist", ""))

    attrs = candidate.get("attributes", {})
    cand_title = normalize(attrs.get("name", ""))
    cand_artist = normalize(attrs.get("artistName", ""))

    if spotify_title == cand_title:
        score += 50
    elif spotify_title in cand_title or cand_title in spotify_title:
        score += 40

    if spotify_artist == cand_artist:
        score += 30
    elif spotify_artist in cand_artist or cand_artist in spotify_artist:
        score += 20

    spotify_duration = spotify_track.get("duration_ms")
    cand_duration = attrs.get("durationInMillis")
    if spotify_duration and cand_duration:
        diff = abs(spotify_duration - cand_duration)
        if diff <= 1000:
            score += 20
        elif diff <= 3000:
            score += 15
        elif diff <= 7000:
            score += 8

    return score


def build_shazam_url(song_id: str, song_name: str) -> str:
    slug = slugify(song_name)
    return f"https://www.shazam.com/song/{song_id}/{slug}"


def find_best_shazam_match(spotify_track: dict, country: str = COUNTRY) -> dict | None:
    search_term = f"{spotify_track.get('main_artist', '')} {spotify_track.get('track_name', '')}".strip()
    data = search_shazam_song(search_term, country=country, limit=3)

    songs = data.get("results", {}).get("songs", {}).get("data", [])
    if not songs:
        return None

    ranked = []
    for song in songs:
        score = score_candidate(spotify_track, song)
        ranked.append((score, song))

    ranked.sort(key=lambda x: x[0], reverse=True)
    best_score, best_song = ranked[0]

    attrs = best_song.get("attributes", {})
    song_id = best_song.get("id")
    song_name = attrs.get("name", "")

    return {
        "spotify_track_name": spotify_track.get("track_name"),
        "spotify_artist_name": spotify_track.get("main_artist"),
        "matched_score": best_score,
        "song_id": song_id,
        "song_name": song_name,
        "artist_name": attrs.get("artistName"),
        "album_name": attrs.get("albumName"),
        "duration_ms": attrs.get("durationInMillis"),
        "apple_music_url": attrs.get("url"),
        "shazam_url": build_shazam_url(song_id, song_name),
    }


def find_multiple_shazam_matches(spotify_tracks: list[dict], country: str = COUNTRY) -> list[dict]:
    results = []

    for track in spotify_tracks:
        match = find_best_shazam_match(track, country=country)
        if match is not None:
            results.append(match)

    return results