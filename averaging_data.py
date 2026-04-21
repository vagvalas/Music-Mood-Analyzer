from statistics import mean

RAW_KEYS = [
    "melodicness",
    "acousticness",
    "valence",
    "danceability",
    "energy",
    "bpm",
]

DERIVED_KEYS = [
    "arousal",
    "positivity",
    "expressiveness",
    "movement",
]


def average_metric(items: list[dict], key: str) -> float | None:
    values = [item[key] for item in items if key in item and item[key] is not None]
    if not values:
        return None
    return round(mean(values), 2)


def aggregate_feature_data(song_results: list[dict]) -> dict:
    if not song_results:
        return {
            "total_songs": 0,
            "raw_averages": {},
            "derived_averages": {},
        }

    feature_rows = [
        song["features"]
        for song in song_results
        if isinstance(song, dict)
        and "features" in song
        and isinstance(song["features"], dict)
    ]

    raw_averages = {
        key: average_metric(feature_rows, key)
        for key in RAW_KEYS
    }

    derived_averages = {
        key: average_metric(feature_rows, key)
        for key in DERIVED_KEYS
    }

    return {
        "total_songs": len(feature_rows),
        "raw_averages": raw_averages,
        "derived_averages": derived_averages,
    }