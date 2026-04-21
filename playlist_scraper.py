from spotify_scraper import SpotifyClient


def get_playlist_tracks(playlist_url: str) -> list[dict]:
    client = SpotifyClient()

    try:
        playlist = client.get_playlist_info(playlist_url)
        tracks = playlist.get("tracks", [])

        results = []

        for track in tracks:
            artists = track.get("artists", [])
            artist_names = [artist.get("name") for artist in artists if artist.get("name")]

            results.append({
                "playlist_url": playlist_url,
                "playlist_name": playlist.get("name"),
                "track_name": track.get("name"),
                "track_id": track.get("id"),
                "track_url": f"https://open.spotify.com/track/{track.get('id')}" if track.get("id") else None,
                "artists": artist_names,
                "main_artist": artist_names[0] if artist_names else None,
                "duration_ms": track.get("duration_ms"),
                "album_name": track.get("album", {}).get("name") if isinstance(track.get("album"), dict) else None,
            })

        return results

    finally:
        client.close()


def get_multiple_playlists_tracks(playlist_urls: list[str]) -> list[dict]:
    all_tracks = []

    for playlist_url in playlist_urls:
        playlist_tracks = get_playlist_tracks(playlist_url)
        all_tracks.extend(playlist_tracks)

    return all_tracks