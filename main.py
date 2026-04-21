import json
import time

from profile_scraper import get_user_playlists_sync
from averaging_data import aggregate_feature_data
from model_analyzer import analyze_averaged_profile
from playlist_scraper import get_playlist_tracks, get_multiple_playlists_tracks
from shazam_query import find_best_shazam_match
from shazam_scraper import extract_features


def main():
    mode = input("Choose mode (profile / playlist): ").strip().lower()
    all_results = []

    if mode == "profile":
        user_url = input("Enter Spotify profile URL: ").strip()
        playlist_urls = get_user_playlists_sync(user_url)

        print(f"\nFound {len(playlist_urls)} playlists.\n")
        for url in playlist_urls:
            print(url)

        tracks = get_multiple_playlists_tracks(playlist_urls)

        print(f"\nCollected {len(tracks)} total tracks from profile playlists.\n")

    elif mode == "playlist":
        playlist_url = input("Enter Spotify playlist URL: ").strip()
        tracks = get_playlist_tracks(playlist_url)

        print(f"\nCollected {len(tracks)} tracks from playlist.\n")

    else:
        print("Invalid mode. Please choose 'profile' or 'playlist'.")
        return

    print("Starting Shazam matching + feature scraping...\n")

    for i, track in enumerate(tracks, start=1):
        track_name = track.get("track_name")
        artist_name = track.get("main_artist")

        print(f"[{i}/{len(tracks)}] {artist_name} - {track_name}")

        match = find_best_shazam_match(track)
        if not match:
            print("  No Shazam match found\n")
            continue

        shazam_url = match["shazam_url"]
        print(f"  Shazam: {shazam_url}")

        features = extract_features(shazam_url)
        if not features:
            print("  No feature data found\n")
            continue

        result = {
            "playlist_name": track.get("playlist_name"),
            "spotify_track_name": track_name,
            "spotify_artist_name": artist_name,
            "spotify_track_id": track.get("track_id"),
            "spotify_track_url": track.get("track_url"),
            "duration_ms": track.get("duration_ms"),
            "album_name": track.get("album_name"),
            "shazam_url": shazam_url,
            "matched_song_name": match.get("song_name"),
            "matched_artist_name": match.get("artist_name"),
            "matched_score": match.get("matched_score"),
            "features": features,
        }

        all_results.append(result)
        print(f"  Features: {features}\n")

        #time.sleep(0.5)

    with open("features_data.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(all_results)} matched songs with features to features_data.json")

    # -------- AGGREGATE --------
    

    summary = aggregate_feature_data(all_results)

    print("\n===== AVERAGED PROFILE =====\n")
    print(json.dumps(summary, indent=2))


    # -------- SAVE SUMMARY --------
    with open("averages.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\nSaved averages to averages.json")


    profile = analyze_averaged_profile(summary)

    print("\n===== FINAL MODEL PROFILE =====\n")
    print(json.dumps(profile, indent=2, ensure_ascii=False))

    with open("model_profile.json", "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()